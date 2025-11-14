"""
Service Layer para el módulo de bajas de inventario.

Contiene la lógica de negocio siguiendo el principio de
Single Responsibility (SOLID). Las operaciones críticas
usan transacciones atómicas para garantizar consistencia.
"""
from typing import Optional
from decimal import Decimal
from datetime import date
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from core.utils import generar_codigo_unico
from .models import (
    MotivoBaja, EstadoBaja, BajaInventario,
    DetalleBaja, HistorialBaja
)
from .repositories import (
    MotivoBajaRepository, EstadoBajaRepository, BajaInventarioRepository,
    DetalleBajaRepository, HistorialBajaRepository
)
from apps.bodega.models import Bodega
from apps.activos.models import Activo


# ==================== BAJA INVENTARIO SERVICE ====================

class BajaInventarioService:
    """Service para lógica de negocio de Bajas de Inventario."""

    def __init__(self):
        self.baja_repo = BajaInventarioRepository()
        self.estado_repo = EstadoBajaRepository()
        self.motivo_repo = MotivoBajaRepository()
        self.detalle_repo = DetalleBajaRepository()
        self.historial_repo = HistorialBajaRepository()

    @transaction.atomic
    def crear_baja(
        self,
        motivo: MotivoBaja,
        bodega: Bodega,
        solicitante: User,
        fecha_baja: date,
        descripcion: str,
        numero: Optional[str] = None,
        **kwargs
    ) -> BajaInventario:
        """
        Crea una nueva baja de inventario.

        Args:
            motivo: Motivo de la baja
            bodega: Bodega
            solicitante: Usuario solicitante
            fecha_baja: Fecha de la baja
            descripcion: Descripción de la baja
            numero: Número de baja (opcional, se genera automático)
            **kwargs: Campos opcionales

        Returns:
            BajaInventario: Baja creada

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validaciones
        errors = {}

        # Validar fecha de baja
        if fecha_baja > date.today():
            errors['fecha_baja'] = 'La fecha de baja no puede ser futura'

        # Validar documento si se requiere
        if motivo.requiere_documento and not kwargs.get('documento'):
            errors['documento'] = 'Este motivo requiere un documento de respaldo'

        if errors:
            raise ValidationError(errors)

        # Generar número si no se proporciona
        if not numero:
            numero = generar_codigo_unico('BAJA', BajaInventario, 'numero', longitud=8)
        else:
            if self.baja_repo.exists_by_numero(numero):
                raise ValidationError({'numero': 'Ya existe una baja con este número'})

        # Obtener estado inicial
        estado_inicial = self.estado_repo.get_inicial()
        if not estado_inicial:
            raise ValidationError('No se ha configurado un estado inicial para bajas de inventario')

        # Crear baja
        baja = BajaInventario.objects.create(
            numero=numero,
            fecha_baja=fecha_baja,
            motivo=motivo,
            estado=estado_inicial,
            bodega=bodega,
            solicitante=solicitante,
            descripcion=descripcion,
            observaciones=kwargs.get('observaciones', ''),
            documento=kwargs.get('documento'),
            valor_total=Decimal('0')
        )

        # Registrar en historial
        self.historial_repo.create(
            baja=baja,
            estado_anterior=None,
            estado_nuevo=estado_inicial,
            usuario=solicitante,
            observaciones=f'Baja de inventario creada por {solicitante.get_full_name()}'
        )

        return baja

    @transaction.atomic
    def cambiar_estado(
        self,
        baja: BajaInventario,
        nuevo_estado: EstadoBaja,
        usuario: User,
        observaciones: str = ''
    ) -> BajaInventario:
        """
        Cambia el estado de una baja y registra en historial.

        Args:
            baja: Baja a actualizar
            nuevo_estado: Nuevo estado
            usuario: Usuario que realiza el cambio
            observaciones: Observaciones del cambio

        Returns:
            BajaInventario: Baja actualizada

        Raises:
            ValidationError: Si el cambio no es válido
        """
        # Validar que no esté en estado final
        if baja.estado.es_final:
            raise ValidationError('No se puede cambiar el estado de una baja finalizada')

        estado_anterior = baja.estado

        # Actualizar estado
        baja.estado = nuevo_estado
        baja.save()

        # Registrar en historial
        self.historial_repo.create(
            baja=baja,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            usuario=usuario,
            observaciones=observaciones
        )

        return baja

    @transaction.atomic
    def autorizar_baja(
        self,
        baja: BajaInventario,
        autorizador: User,
        notas_autorizacion: str = ''
    ) -> BajaInventario:
        """
        Autoriza una baja de inventario.

        Args:
            baja: Baja a autorizar
            autorizador: Usuario autorizador
            notas_autorizacion: Notas de autorización

        Returns:
            BajaInventario: Baja autorizada

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar que no esté ya autorizada
        if baja.autorizador:
            raise ValidationError('Esta baja ya fue autorizada')

        # Validar que requiera autorización
        if not baja.motivo.requiere_autorizacion:
            raise ValidationError('Esta baja no requiere autorización')

        # Validar que tenga detalles
        detalles = self.detalle_repo.filter_by_baja(baja)
        if not detalles.exists():
            raise ValidationError('La baja no tiene detalles para autorizar')

        # Actualizar baja
        baja.autorizador = autorizador
        baja.fecha_autorizacion = timezone.now()
        baja.notas_autorizacion = notas_autorizacion

        # Cambiar a estado autorizado
        estado_autorizado = self.estado_repo.get_by_codigo('AUTORIZADO')
        if not estado_autorizado:
            raise ValidationError('No existe el estado AUTORIZADO en el sistema')

        estado_anterior = baja.estado
        baja.estado = estado_autorizado
        baja.save()

        # Registrar en historial
        self.historial_repo.create(
            baja=baja,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_autorizado,
            usuario=autorizador,
            observaciones=f'Autorizada por {autorizador.get_full_name()}. {notas_autorizacion}'
        )

        return baja

    @transaction.atomic
    def rechazar_baja(
        self,
        baja: BajaInventario,
        rechazador: User,
        motivo_rechazo: str
    ) -> BajaInventario:
        """
        Rechaza una baja de inventario.

        Args:
            baja: Baja a rechazar
            rechazador: Usuario que rechaza
            motivo_rechazo: Motivo del rechazo

        Returns:
            BajaInventario: Baja rechazada

        Raises:
            ValidationError: Si hay errores de validación
        """
        if not motivo_rechazo:
            raise ValidationError({'motivo_rechazo': 'Debe indicar el motivo del rechazo'})

        # Cambiar a estado rechazado
        estado_rechazado = self.estado_repo.get_by_codigo('RECHAZADO')
        if not estado_rechazado:
            raise ValidationError('No existe el estado RECHAZADO en el sistema')

        estado_anterior = baja.estado
        baja.estado = estado_rechazado
        baja.notas_autorizacion = f'RECHAZADO: {motivo_rechazo}'
        baja.save()

        # Registrar en historial
        self.historial_repo.create(
            baja=baja,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_rechazado,
            usuario=rechazador,
            observaciones=f'Rechazada por {rechazador.get_full_name()}. Motivo: {motivo_rechazo}'
        )

        return baja

    @transaction.atomic
    def confirmar_baja(
        self,
        baja: BajaInventario,
        usuario: User
    ) -> BajaInventario:
        """
        Confirma y finaliza una baja de inventario.

        Args:
            baja: Baja a confirmar
            usuario: Usuario que confirma

        Returns:
            BajaInventario: Baja confirmada

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar que esté autorizada si requiere autorización
        if baja.motivo.requiere_autorizacion and not baja.autorizador:
            raise ValidationError('La baja debe estar autorizada antes de confirmarla')

        # Validar que tenga detalles
        detalles = self.detalle_repo.filter_by_baja(baja)
        if not detalles.exists():
            raise ValidationError('La baja no tiene detalles para confirmar')

        # Cambiar a estado confirmado
        estado_confirmado = self.estado_repo.get_by_codigo('CONFIRMADO')
        if not estado_confirmado:
            raise ValidationError('No existe el estado CONFIRMADO en el sistema')

        estado_anterior = baja.estado
        baja.estado = estado_confirmado
        baja.save()

        # Registrar en historial
        self.historial_repo.create(
            baja=baja,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_confirmado,
            usuario=usuario,
            observaciones=f'Baja confirmada por {usuario.get_full_name()}'
        )

        return baja

    @transaction.atomic
    def recalcular_total(self, baja: BajaInventario) -> BajaInventario:
        """
        Recalcula el valor total de la baja basándose en sus detalles.

        Args:
            baja: Baja de inventario

        Returns:
            BajaInventario: Baja actualizada
        """
        detalles = self.detalle_repo.filter_by_baja(baja)
        total = sum(d.valor_total for d in detalles)

        baja.valor_total = total
        baja.save()

        return baja


# ==================== DETALLE BAJA SERVICE ====================

class DetalleBajaService:
    """Service para lógica de negocio de Detalles de Baja."""

    def __init__(self):
        self.detalle_repo = DetalleBajaRepository()
        self.baja_repo = BajaInventarioRepository()

    @transaction.atomic
    def agregar_detalle(
        self,
        baja: BajaInventario,
        activo: Activo,
        cantidad: Decimal,
        valor_unitario: Decimal,
        **kwargs
    ) -> DetalleBaja:
        """
        Agrega un detalle a una baja de inventario.

        Args:
            baja: Baja de inventario
            activo: Activo a dar de baja
            cantidad: Cantidad
            valor_unitario: Valor unitario
            **kwargs: Campos opcionales (lote, numero_serie, observaciones)

        Returns:
            DetalleBaja: Detalle creado

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar que la baja no esté finalizada
        if baja.estado.es_final:
            raise ValidationError('No se pueden agregar detalles a una baja finalizada')

        # Validar cantidad
        if cantidad <= 0:
            raise ValidationError({'cantidad': 'La cantidad debe ser mayor a cero'})

        # Validar valor unitario
        if valor_unitario < 0:
            raise ValidationError({'valor_unitario': 'El valor unitario no puede ser negativo'})

        # Crear detalle
        detalle = DetalleBaja.objects.create(
            baja=baja,
            activo=activo,
            cantidad=cantidad,
            valor_unitario=valor_unitario,
            valor_total=cantidad * valor_unitario,
            lote=kwargs.get('lote', ''),
            numero_serie=kwargs.get('numero_serie', ''),
            observaciones=kwargs.get('observaciones', '')
        )

        # Recalcular total de la baja
        baja_service = BajaInventarioService()
        baja_service.recalcular_total(baja)

        return detalle

    @transaction.atomic
    def eliminar_detalle(self, detalle: DetalleBaja) -> None:
        """
        Elimina (soft delete) un detalle.

        Args:
            detalle: Detalle a eliminar

        Raises:
            ValidationError: Si la baja está finalizada
        """
        # Validar que la baja no esté finalizada
        if detalle.baja.estado.es_final:
            raise ValidationError('No se pueden eliminar detalles de una baja finalizada')

        # Soft delete
        detalle.eliminado = True
        detalle.activo = False
        detalle.save()

        # Recalcular total de la baja
        baja_service = BajaInventarioService()
        baja_service.recalcular_total(detalle.baja)

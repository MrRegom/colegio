"""
Service Layer para el módulo de solicitudes.

Contiene la lógica de negocio siguiendo el principio de
Single Responsibility (SOLID). Las operaciones críticas
usan transacciones atómicas para garantizar consistencia.
"""
from typing import Optional, List, Dict, Any
from decimal import Decimal
from datetime import date, datetime
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from core.utils import generar_codigo_unico
from .models import (
    Departamento, Area, Equipo,
    TipoSolicitud, EstadoSolicitud, Solicitud,
    DetalleSolicitud, HistorialSolicitud
)
from .repositories import (
    DepartamentoRepository, AreaRepository, EquipoRepository,
    TipoSolicitudRepository, EstadoSolicitudRepository, SolicitudRepository,
    DetalleSolicitudRepository, HistorialSolicitudRepository
)
from apps.bodega.models import Bodega
from apps.activos.models import Activo


# ==================== SOLICITUD SERVICE ====================

class SolicitudService:
    """Service para lógica de negocio de Solicitudes."""

    def __init__(self):
        self.solicitud_repo = SolicitudRepository()
        self.estado_repo = EstadoSolicitudRepository()
        self.tipo_repo = TipoSolicitudRepository()
        self.detalle_repo = DetalleSolicitudRepository()
        self.historial_repo = HistorialSolicitudRepository()

    @transaction.atomic
    def crear_solicitud(
        self,
        tipo_solicitud: TipoSolicitud,
        solicitante: User,
        fecha_requerida: date,
        motivo: str,
        area_solicitante: str,
        titulo_actividad: str,
        objetivo_actividad: str,
        tipo_choice: str = 'ARTICULO',
        bodega_origen: Optional[Bodega] = None,
        departamento: Optional[Departamento] = None,
        area: Optional[Area] = None,
        equipo: Optional[Equipo] = None,
        numero: Optional[str] = None,
        **kwargs: Any
    ) -> Solicitud:
        """
        Crea una nueva solicitud.

        Args:
            tipo_solicitud: Tipo de solicitud
            solicitante: Usuario solicitante
            fecha_requerida: Fecha en que se requiere
            motivo: Motivo de la solicitud
            area_solicitante: Área del solicitante
            titulo_actividad: Título de la actividad
            objetivo_actividad: Objetivo de la actividad
            tipo_choice: 'ACTIVO' o 'ARTICULO'
            bodega_origen: Bodega origen (solo para artículos)
            departamento: Departamento (opcional)
            area: Área (opcional)
            equipo: Equipo (opcional)
            numero: Número de solicitud (opcional, se genera automático)
            **kwargs: Campos opcionales

        Returns:
            Solicitud: Solicitud creada

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validaciones
        errors = {}

        # Los campos titulo_actividad y objetivo_actividad son opcionales
        # Solo se validan si se proporcionan y tienen contenido

        # Validar fecha requerida
        if fecha_requerida < date.today():
            errors['fecha_requerida'] = 'La fecha requerida no puede ser anterior a hoy'

        # Validar bodega para artículos
        if tipo_choice == 'ARTICULO' and not bodega_origen:
            errors['bodega_origen'] = 'Las solicitudes de artículos requieren bodega de origen'

        if errors:
            raise ValidationError(errors)

        # Generar número si no se proporciona
        if not numero:
            numero = generar_codigo_unico('SOL', Solicitud, 'numero', longitud=8)
        else:
            if self.solicitud_repo.exists_by_numero(numero):
                raise ValidationError({'numero': 'Ya existe una solicitud con este número'})

        # Obtener estado inicial
        estado_inicial = self.estado_repo.get_inicial()
        if not estado_inicial:
            raise ValidationError('No se ha configurado un estado inicial para solicitudes')

        # Crear solicitud
        solicitud = Solicitud.objects.create(
            tipo=tipo_choice,
            numero=numero,
            fecha_requerida=fecha_requerida,
            tipo_solicitud=tipo_solicitud,
            estado=estado_inicial,
            solicitante=solicitante,
            area_solicitante=area_solicitante,
            titulo_actividad=titulo_actividad,
            objetivo_actividad=objetivo_actividad,
            departamento=departamento,
            area=area,
            equipo=equipo,
            bodega_origen=bodega_origen,
            motivo=motivo,
            observaciones=kwargs.get('observaciones', '')
        )

        # Registrar en historial
        self.historial_repo.create(
            solicitud=solicitud,
            estado_anterior=None,
            estado_nuevo=estado_inicial,
            usuario=solicitante,
            observaciones=f'Solicitud creada por {solicitante.get_full_name()}'
        )

        return solicitud

    @transaction.atomic
    def cambiar_estado(
        self,
        solicitud: Solicitud,
        nuevo_estado: EstadoSolicitud,
        usuario: User,
        observaciones: str = ''
    ) -> Solicitud:
        """
        Cambia el estado de una solicitud y registra en historial.

        Args:
            solicitud: Solicitud a actualizar
            nuevo_estado: Nuevo estado
            usuario: Usuario que realiza el cambio
            observaciones: Observaciones del cambio

        Returns:
            Solicitud: Solicitud actualizada

        Raises:
            ValidationError: Si el cambio no es válido
        """
        # Validar que no esté en estado final
        if solicitud.estado.es_final:
            raise ValidationError('No se puede cambiar el estado de una solicitud finalizada')

        estado_anterior = solicitud.estado

        # Actualizar estado
        solicitud.estado = nuevo_estado
        solicitud.save()

        # Registrar en historial
        self.historial_repo.create(
            solicitud=solicitud,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            usuario=usuario,
            observaciones=observaciones
        )

        return solicitud

    @transaction.atomic
    def aprobar_solicitud(
        self,
        solicitud: Solicitud,
        aprobador: User,
        detalles_aprobados: List[Dict[str, Any]],
        notas_aprobacion: str = ''
    ) -> Solicitud:
        """
        Aprueba una solicitud y establece cantidades aprobadas.

        Args:
            solicitud: Solicitud a aprobar
            aprobador: Usuario aprobador
            detalles_aprobados: Lista con {detalle_id, cantidad_aprobada}
            notas_aprobacion: Notas de aprobación

        Returns:
            Solicitud: Solicitud aprobada

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar que no esté ya aprobada
        if solicitud.aprobador:
            raise ValidationError('Esta solicitud ya fue aprobada')

        # Validar que tenga detalles
        detalles = self.detalle_repo.filter_by_solicitud(solicitud)
        if not detalles.exists():
            raise ValidationError('La solicitud no tiene detalles para aprobar')

        # Actualizar cantidades aprobadas
        for detalle_data in detalles_aprobados:
            detalle = self.detalle_repo.get_by_id(detalle_data['detalle_id'])
            if detalle and detalle.solicitud.id == solicitud.id:
                cantidad_aprobada = Decimal(str(detalle_data['cantidad_aprobada']))

                # Validar que no exceda lo solicitado
                if cantidad_aprobada > detalle.cantidad_solicitada:
                    producto = detalle.producto_nombre
                    raise ValidationError(
                        f'La cantidad aprobada para {producto} '
                        f'no puede exceder la cantidad solicitada ({detalle.cantidad_solicitada})'
                    )

                # Validar que no sea negativa
                if cantidad_aprobada < 0:
                    producto = detalle.producto_nombre
                    raise ValidationError(
                        f'La cantidad aprobada para {producto} no puede ser negativa'
                    )

                detalle.cantidad_aprobada = cantidad_aprobada
                detalle.save()

        # Actualizar solicitud
        solicitud.aprobador = aprobador
        solicitud.fecha_aprobacion = timezone.now()
        solicitud.notas_aprobacion = notas_aprobacion

        # Cambiar a estado aprobado
        estado_aprobado = self.estado_repo.get_by_codigo('APROBADA')
        if not estado_aprobado:
            raise ValidationError('No existe el estado APROBADA en el sistema')

        estado_anterior = solicitud.estado
        solicitud.estado = estado_aprobado
        solicitud.save()

        # Registrar en historial
        self.historial_repo.create(
            solicitud=solicitud,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_aprobado,
            usuario=aprobador,
            observaciones=f'Aprobada por {aprobador.get_full_name()}. {notas_aprobacion}'
        )

        return solicitud

    @transaction.atomic
    def rechazar_solicitud(
        self,
        solicitud: Solicitud,
        rechazador: User,
        motivo_rechazo: str
    ) -> Solicitud:
        """
        Rechaza una solicitud.

        Args:
            solicitud: Solicitud a rechazar
            rechazador: Usuario que rechaza
            motivo_rechazo: Motivo del rechazo

        Returns:
            Solicitud: Solicitud rechazada

        Raises:
            ValidationError: Si hay errores de validación
        """
        if not motivo_rechazo:
            raise ValidationError({'motivo_rechazo': 'Debe indicar el motivo del rechazo'})

        # Cambiar a estado rechazado
        estado_rechazado = self.estado_repo.get_by_codigo('RECHAZADA')
        if not estado_rechazado:
            raise ValidationError('No existe el estado RECHAZADA en el sistema')

        estado_anterior = solicitud.estado
        solicitud.estado = estado_rechazado
        solicitud.notas_aprobacion = f'RECHAZADO: {motivo_rechazo}'
        solicitud.save()

        # Registrar en historial
        self.historial_repo.create(
            solicitud=solicitud,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_rechazado,
            usuario=rechazador,
            observaciones=f'Rechazada por {rechazador.get_full_name()}. Motivo: {motivo_rechazo}'
        )

        return solicitud

    @transaction.atomic
    def despachar_solicitud(
        self,
        solicitud: Solicitud,
        despachador: User,
        detalles_despachados: List[Dict[str, Any]],
        notas_despacho: str = ''
    ) -> Solicitud:
        """
        Despacha una solicitud.

        Args:
            solicitud: Solicitud a despachar
            despachador: Usuario despachador
            detalles_despachados: Lista con {detalle_id, cantidad_despachada}
            notas_despacho: Notas de despacho

        Returns:
            Solicitud: Solicitud despachada

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar que esté aprobada
        if not solicitud.aprobador:
            raise ValidationError('Solo se pueden despachar solicitudes aprobadas')

        # Validar que no esté ya despachada
        if solicitud.despachador:
            raise ValidationError('Esta solicitud ya fue despachada')

        # Actualizar cantidades despachadas
        for detalle_data in detalles_despachados:
            detalle = self.detalle_repo.get_by_id(detalle_data['detalle_id'])
            if detalle and detalle.solicitud.id == solicitud.id:
                cantidad_despachada = Decimal(str(detalle_data['cantidad_despachada']))

                # Validar que no exceda lo aprobado
                if cantidad_despachada > detalle.cantidad_aprobada:
                    raise ValidationError(
                        f'La cantidad despachada para {detalle.activo.codigo} '
                        f'excede la cantidad aprobada'
                    )

                detalle.cantidad_despachada = cantidad_despachada
                detalle.save()

        # Actualizar solicitud
        solicitud.despachador = despachador
        solicitud.fecha_despacho = timezone.now()
        solicitud.notas_despacho = notas_despacho

        # Cambiar a estado despachado
        estado_despachado = self.estado_repo.get_by_codigo('DESPACHADA')
        if not estado_despachado:
            raise ValidationError('No existe el estado DESPACHADA en el sistema')

        estado_anterior = solicitud.estado
        solicitud.estado = estado_despachado
        solicitud.save()

        # Registrar en historial
        self.historial_repo.create(
            solicitud=solicitud,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_despachado,
            usuario=despachador,
            observaciones=f'Despachada por {despachador.get_full_name()}. {notas_despacho}'
        )

        return solicitud

    @transaction.atomic
    def cancelar_solicitud(
        self,
        solicitud: Solicitud,
        usuario: User,
        motivo_cancelacion: str
    ) -> Solicitud:
        """
        Cancela una solicitud.

        Args:
            solicitud: Solicitud a cancelar
            usuario: Usuario que cancela
            motivo_cancelacion: Motivo de cancelación

        Returns:
            Solicitud: Solicitud cancelada

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar que no esté finalizada
        if solicitud.estado.es_final:
            raise ValidationError('No se puede cancelar una solicitud finalizada')

        if not motivo_cancelacion:
            raise ValidationError({'motivo_cancelacion': 'Debe indicar el motivo de cancelación'})

        # Cambiar a estado cancelado
        estado_cancelado = self.estado_repo.get_by_codigo('CANCELADA')
        if not estado_cancelado:
            raise ValidationError('No existe el estado CANCELADA en el sistema')

        estado_anterior = solicitud.estado
        solicitud.estado = estado_cancelado
        solicitud.observaciones = f'{solicitud.observaciones}\nCANCELADO: {motivo_cancelacion}'
        solicitud.save()

        # Registrar en historial
        self.historial_repo.create(
            solicitud=solicitud,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_cancelado,
            usuario=usuario,
            observaciones=f'Cancelada por {usuario.get_full_name()}. Motivo: {motivo_cancelacion}'
        )

        return solicitud


# ==================== DETALLE SOLICITUD SERVICE ====================

class DetalleSolicitudService:
    """Service para lógica de negocio de Detalles de Solicitud."""

    def __init__(self):
        self.detalle_repo = DetalleSolicitudRepository()

    @transaction.atomic
    def agregar_detalle(
        self,
        solicitud: Solicitud,
        activo: Activo,
        cantidad_solicitada: Decimal,
        observaciones: str = ''
    ) -> DetalleSolicitud:
        """
        Agrega un detalle a una solicitud.

        Args:
            solicitud: Solicitud
            activo: Activo solicitado
            cantidad_solicitada: Cantidad solicitada
            observaciones: Observaciones

        Returns:
            DetalleSolicitud: Detalle creado

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar que la solicitud no esté finalizada
        if solicitud.estado.es_final:
            raise ValidationError('No se pueden agregar detalles a una solicitud finalizada')

        # Validar cantidad
        if cantidad_solicitada <= 0:
            raise ValidationError({'cantidad_solicitada': 'La cantidad debe ser mayor a cero'})

        # Crear detalle
        detalle = DetalleSolicitud.objects.create(
            solicitud=solicitud,
            activo=activo,
            cantidad_solicitada=cantidad_solicitada,
            cantidad_aprobada=Decimal('0'),
            cantidad_despachada=Decimal('0'),
            observaciones=observaciones
        )

        return detalle

    @transaction.atomic
    def eliminar_detalle(self, detalle: DetalleSolicitud) -> None:
        """
        Elimina (soft delete) un detalle.

        Args:
            detalle: Detalle a eliminar

        Raises:
            ValidationError: Si la solicitud está finalizada
        """
        # Validar que la solicitud no esté finalizada
        if detalle.solicitud.estado.es_final:
            raise ValidationError('No se pueden eliminar detalles de una solicitud finalizada')

        # Soft delete
        detalle.eliminado = True
        detalle.activo = False
        detalle.save()

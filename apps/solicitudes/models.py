from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models

from apps.activos.models import Activo
from apps.bodega.models import Articulo, Bodega
from core.models import BaseModel

User = get_user_model()


class Departamento(BaseModel):
    """
    Catálogo de departamentos de la institución.

    Representa las unidades organizacionales de nivel superior dentro de la institución.
    Cada departamento puede tener un responsable asignado y está vinculado a múltiples
    áreas y equipos de trabajo.

    Attributes:
        codigo: Código único identificador del departamento.
        nombre: Nombre descriptivo del departamento.
        descripcion: Descripción detallada opcional del departamento.
        responsable: Usuario responsable del departamento (opcional).
        activo: Indica si el departamento está activo (heredado de BaseModel).
    """

    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código',
        help_text='Código único del departamento'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        help_text='Nombre descriptivo del departamento'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Descripción detallada del departamento'
    )
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='departamentos_responsable',
        verbose_name='Responsable',
        blank=True,
        null=True,
        help_text='Usuario responsable del departamento'
    )

    class Meta:
        db_table = 'tba_solicitudes_conf_departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['activo', 'eliminado']),
        ]

    def __str__(self) -> str:
        """Representación en cadena del departamento."""
        return f"{self.codigo} - {self.nombre}"


class Area(BaseModel):
    """
    Catálogo de áreas dentro de los departamentos.

    Representa subdivisiones organizacionales dentro de un departamento.
    Cada área pertenece a un departamento y puede tener un responsable asignado.

    Attributes:
        codigo: Código único identificador del área.
        nombre: Nombre descriptivo del área.
        descripcion: Descripción detallada opcional del área.
        departamento: Departamento al que pertenece el área.
        responsable: Usuario responsable del área (opcional).
        activo: Indica si el área está activa (heredado de BaseModel).
    """

    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código',
        help_text='Código único del área'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        help_text='Nombre descriptivo del área'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Descripción detallada del área'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        related_name='areas',
        verbose_name='Departamento',
        help_text='Departamento al que pertenece el área'
    )
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='areas_responsable',
        verbose_name='Responsable',
        blank=True,
        null=True,
        help_text='Usuario responsable del área'
    )

    class Meta:
        db_table = 'tba_solicitudes_conf_area'
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['departamento']),
            models.Index(fields=['activo', 'eliminado']),
        ]

    def __str__(self) -> str:
        """Representación en cadena del área."""
        return f"{self.codigo} - {self.nombre}"


class Equipo(BaseModel):
    """
    Catálogo de equipos de trabajo.

    Representa grupos de trabajo dentro de un departamento.
    Cada equipo tiene un líder asignado y pertenece a un departamento específico.

    Attributes:
        codigo: Código único identificador del equipo.
        nombre: Nombre descriptivo del equipo.
        descripcion: Descripción detallada opcional del equipo.
        departamento: Departamento al que pertenece el equipo.
        lider: Usuario líder del equipo (opcional).
        activo: Indica si el equipo está activo (heredado de BaseModel).
    """

    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código',
        help_text='Código único del equipo'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        help_text='Nombre descriptivo del equipo'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Descripción detallada del equipo'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        related_name='equipos',
        verbose_name='Departamento',
        help_text='Departamento al que pertenece el equipo'
    )
    lider = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='equipos_lider',
        verbose_name='Líder',
        blank=True,
        null=True,
        help_text='Usuario líder del equipo'
    )

    class Meta:
        db_table = 'tba_solicitudes_conf_equipo'
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['departamento']),
            models.Index(fields=['activo', 'eliminado']),
        ]

    def __str__(self) -> str:
        """Representación en cadena del equipo."""
        return f"{self.codigo} - {self.nombre}"


class TipoSolicitud(BaseModel):
    """
    Catálogo de tipos de solicitud.

    Define los diferentes tipos de solicitudes que pueden realizarse en el sistema.
    Cada tipo puede requerir o no aprobación según su configuración.

    Attributes:
        codigo: Código único identificador del tipo de solicitud.
        nombre: Nombre descriptivo del tipo de solicitud.
        descripcion: Descripción detallada opcional del tipo.
        requiere_aprobacion: Indica si el tipo requiere aprobación.
        activo: Indica si el tipo está activo (heredado de BaseModel).
    """

    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código',
        help_text='Código único del tipo de solicitud'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        help_text='Nombre descriptivo del tipo'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Descripción detallada del tipo'
    )
    requiere_aprobacion = models.BooleanField(
        default=True,
        verbose_name='Requiere Aprobación',
        help_text='Indica si las solicitudes de este tipo requieren aprobación'
    )

    class Meta:
        db_table = 'tba_solicitudes_conf_tipo'
        verbose_name = 'Tipo de Solicitud'
        verbose_name_plural = 'Tipos de Solicitud'
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['activo', 'eliminado']),
        ]

    def __str__(self) -> str:
        """Representación en cadena del tipo de solicitud."""
        return f"{self.codigo} - {self.nombre}"


class EstadoSolicitud(BaseModel):
    """
    Catálogo de estados de solicitudes.

    Define los diferentes estados por los que puede pasar una solicitud.
    Incluye estados iniciales, finales y estados que requieren acción.

    Attributes:
        codigo: Código único identificador del estado.
        nombre: Nombre descriptivo del estado.
        descripcion: Descripción detallada opcional del estado.
        color: Color hexadecimal para representar visualmente el estado.
        es_inicial: Indica si es un estado inicial.
        es_final: Indica si es un estado final.
        requiere_accion: Indica si el estado requiere acción del usuario.
        activo: Indica si el estado está activo (heredado de BaseModel).
    """

    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código',
        help_text='Código único del estado'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        help_text='Nombre descriptivo del estado'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Descripción detallada del estado'
    )
    color = models.CharField(
        max_length=7,
        default='#6c757d',
        verbose_name='Color (Hex)',
        help_text='Color hexadecimal para representación visual'
    )
    es_inicial = models.BooleanField(
        default=False,
        verbose_name='Estado Inicial',
        help_text='Indica si es un estado inicial'
    )
    es_final = models.BooleanField(
        default=False,
        verbose_name='Estado Final',
        help_text='Indica si es un estado final'
    )
    requiere_accion = models.BooleanField(
        default=False,
        verbose_name='Requiere Acción',
        help_text='Indica si el estado requiere acción del usuario'
    )

    class Meta:
        db_table = 'tba_solicitudes_conf_estado'
        verbose_name = 'Estado de Solicitud'
        verbose_name_plural = 'Estados de Solicitudes'
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['es_inicial']),
            models.Index(fields=['es_final']),
            models.Index(fields=['activo', 'eliminado']),
        ]

    def __str__(self) -> str:
        """Representación en cadena del estado."""
        return f"{self.codigo} - {self.nombre}"


class Solicitud(BaseModel):
    """
    Modelo para gestionar solicitudes de materiales y activos.

    Representa una solicitud de materiales (artículos) o activos (bienes) realizada
    por un usuario. Incluye información sobre la actividad, el solicitante, el estado
    del proceso de aprobación y despacho.

    Attributes:
        tipo: Tipo de solicitud (ACTIVO o ARTICULO).
        numero: Número único de la solicitud.
        fecha_solicitud: Fecha y hora de creación de la solicitud.
        fecha_requerida: Fecha en que se requieren los materiales.
        tipo_solicitud: Tipo de solicitud según catálogo.
        estado: Estado actual de la solicitud.
        titulo_actividad: Título de la actividad asociada (opcional).
        objetivo_actividad: Objetivo de la actividad (opcional).
        solicitante: Usuario que realiza la solicitud.
        area_solicitante: Nombre del área que solicita.
        departamento: Departamento asociado (opcional).
        area: Área asociada (opcional).
        equipo: Equipo asociado (opcional).
        aprobador: Usuario que aprueba la solicitud (opcional).
        fecha_aprobacion: Fecha de aprobación (opcional).
        despachador: Usuario que despacha la solicitud (opcional).
        fecha_despacho: Fecha de despacho (opcional).
        bodega_origen: Bodega desde donde se despachan los artículos (solo para artículos).
        motivo: Motivo de la solicitud.
        observaciones: Observaciones adicionales (opcional).
        notas_aprobacion: Notas del aprobador (opcional).
        notas_despacho: Notas del despachador (opcional).
    """

    TIPO_CHOICES = [
        ('ACTIVO', 'Solicitud de Activos/Bienes'),
        ('ARTICULO', 'Solicitud de Artículos'),
    ]

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default='ARTICULO',
        verbose_name='Tipo',
        help_text='Define si la solicitud es de activos (bienes) o artículos'
    )
    numero = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Solicitud',
        help_text='Número único de la solicitud'
    )
    fecha_solicitud = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Solicitud',
        help_text='Fecha y hora de creación de la solicitud'
    )
    fecha_requerida = models.DateField(
        verbose_name='Fecha Requerida',
        help_text='Fecha en que se requieren los materiales'
    )

    tipo_solicitud = models.ForeignKey(
        TipoSolicitud,
        on_delete=models.PROTECT,
        related_name='solicitudes',
        verbose_name='Tipo de Solicitud',
        help_text='Tipo de solicitud según catálogo'
    )
    estado = models.ForeignKey(
        EstadoSolicitud,
        on_delete=models.PROTECT,
        related_name='solicitudes',
        verbose_name='Estado',
        help_text='Estado actual de la solicitud'
    )

    # Información de la actividad
    titulo_actividad = models.CharField(
        max_length=200,
        verbose_name='Título de la Actividad',
        help_text='Título descriptivo de la actividad para la cual se solicitan los materiales',
        blank=True,
        null=True
    )
    objetivo_actividad = models.TextField(
        verbose_name='Objetivo de la Actividad',
        help_text='Objetivo que se busca alcanzar con esta actividad',
        blank=True,
        null=True
    )

    # Solicitante y responsables
    solicitante = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='solicitudes_realizadas',
        verbose_name='Solicitante',
        help_text='Usuario que realiza la solicitud'
    )
    area_solicitante = models.CharField(
        max_length=100,
        verbose_name='Área Solicitante',
        help_text='Nombre del área que solicita'
    )

    # Referencias a las estructuras organizacionales
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT,
        related_name='solicitudes',
        verbose_name='Departamento',
        blank=True,
        null=True,
        help_text='Departamento asociado a la solicitud'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name='solicitudes',
        verbose_name='Área',
        blank=True,
        null=True,
        help_text='Área asociada a la solicitud'
    )
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name='solicitudes',
        verbose_name='Equipo',
        blank=True,
        null=True,
        help_text='Equipo asociado a la solicitud'
    )

    aprobador = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='solicitudes_aprobadas',
        verbose_name='Aprobador',
        blank=True,
        null=True,
        help_text='Usuario que aprobó la solicitud'
    )
    fecha_aprobacion = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Fecha de Aprobación',
        help_text='Fecha y hora de aprobación'
    )

    despachador = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='solicitudes_despachadas',
        verbose_name='Despachador',
        blank=True,
        null=True,
        help_text='Usuario que despachó la solicitud'
    )
    fecha_despacho = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Fecha de Despacho',
        help_text='Fecha y hora de despacho'
    )

    # Bodega (solo para solicitudes de artículos)
    bodega_origen = models.ForeignKey(
        Bodega,
        on_delete=models.PROTECT,
        related_name='solicitudes_origen',
        verbose_name='Bodega Origen',
        blank=True,
        null=True,
        help_text='Solo requerido para solicitudes de artículos. Las solicitudes de activos no tienen bodega.'
    )

    # Descripción y observaciones
    motivo = models.TextField(
        verbose_name='Motivo de la Solicitud',
        help_text='Justificación de la solicitud'
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones',
        help_text='Observaciones adicionales'
    )
    notas_aprobacion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas de Aprobación',
        help_text='Notas del aprobador'
    )
    notas_despacho = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas de Despacho',
        help_text='Notas del despachador'
    )

    class Meta:
        db_table = 'tba_solicitudes_solicitud'
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
        ordering = ['-fecha_solicitud', '-numero']
        permissions = [
            ('aprobar_solicitud', 'Puede aprobar solicitudes'),
            ('rechazar_solicitud', 'Puede rechazar solicitudes'),
            ('despachar_solicitud', 'Puede despachar solicitudes'),
            ('change_any_solicitud', 'Puede editar cualquier solicitud'),
            ('delete_any_solicitud', 'Puede eliminar cualquier solicitud'),
            ('ver_todas_solicitudes', 'Puede ver todas las solicitudes'),
        ]
        indexes = [
            models.Index(fields=['numero']),
            models.Index(fields=['tipo']),
            models.Index(fields=['fecha_solicitud']),
            models.Index(fields=['fecha_requerida']),
            models.Index(fields=['solicitante']),
            models.Index(fields=['estado']),
            models.Index(fields=['tipo_solicitud']),
            models.Index(fields=['activo', 'eliminado']),
        ]

    def __str__(self) -> str:
        """Representación en cadena de la solicitud."""
        return f"SOL-{self.numero} - {self.solicitante.email}"


class DetalleSolicitud(BaseModel):
    """
    Modelo para el detalle de artículos o bienes solicitados.

    Representa cada línea de detalle dentro de una solicitud, especificando
    el artículo o activo solicitado y las cantidades en cada etapa del proceso.

    Attributes:
        solicitud: Solicitud a la que pertenece el detalle.
        articulo: Artículo solicitado (para solicitudes de artículos).
        activo: Activo/bien solicitado (para solicitudes de activos).
        cantidad_solicitada: Cantidad solicitada inicialmente.
        cantidad_aprobada: Cantidad aprobada por el aprobador.
        cantidad_despachada: Cantidad efectivamente despachada.
        observaciones: Observaciones específicas del detalle (opcional).

    Note:
        Solo uno de los campos articulo o activo debe estar presente.
        Esto se valida en el método clean().
    """

    solicitud = models.ForeignKey(
        Solicitud,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Solicitud',
        help_text='Solicitud a la que pertenece el detalle'
    )
    # FK a Artículo de Bodega (para solicitudes de artículos)
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.PROTECT,
        related_name='detalles_solicitud',
        verbose_name='Artículo',
        blank=True,
        null=True,
        help_text='Artículo solicitado (solo para solicitudes de artículos)'
    )
    # FK a Activo/Bien de Inventario (para solicitudes de bienes)
    activo = models.ForeignKey(
        Activo,
        on_delete=models.PROTECT,
        related_name='detalles_solicitud',
        verbose_name='Bien/Activo',
        blank=True,
        null=True,
        help_text='Bien o activo solicitado (solo para solicitudes de activos)'
    )
    cantidad_solicitada = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Cantidad Solicitada',
        help_text='Cantidad solicitada del artículo o activo'
    )
    cantidad_aprobada = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Cantidad Aprobada',
        help_text='Cantidad aprobada por el aprobador'
    )
    cantidad_despachada = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Cantidad Despachada',
        help_text='Cantidad efectivamente despachada'
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones',
        help_text='Observaciones específicas del detalle'
    )

    class Meta:
        db_table = 'tba_solicitudes_detalle'
        verbose_name = 'Detalle de Solicitud'
        verbose_name_plural = 'Detalles de Solicitudes'
        ordering = ['solicitud', 'id']
        indexes = [
            models.Index(fields=['solicitud']),
            models.Index(fields=['articulo']),
            models.Index(fields=['activo']),
        ]

    def __str__(self) -> str:
        """Representación en cadena del detalle."""
        producto = self.articulo or self.activo
        codigo = producto.codigo if producto else 'N/A'
        return f"{self.solicitud.numero} - {codigo} ({self.cantidad_solicitada})"

    def clean(self) -> None:
        """
        Validación personalizada del modelo.

        Verifica que solo uno de los campos articulo o activo esté presente,
        pero no ambos simultáneamente.

        Raises:
            ValidationError: Si no se especifica artículo ni activo, o si se
                especifican ambos simultáneamente.
        """
        super().clean()

        if not self.articulo and not self.activo:
            raise ValidationError(
                'Debe especificar un artículo o un bien/activo'
            )

        if self.articulo and self.activo:
            raise ValidationError(
                'No puede especificar tanto artículo como bien/activo simultáneamente'
            )

    @property
    def producto_nombre(self) -> str:
        """
        Obtiene el nombre del producto (artículo o activo).

        Returns:
            str: Nombre del artículo o activo asociado.
        """
        return self.articulo.nombre if self.articulo else self.activo.nombre

    @property
    def producto_codigo(self) -> str:
        """
        Obtiene el código del producto (artículo o activo).

        Returns:
            str: Código del artículo o activo asociado.
        """
        return self.articulo.codigo if self.articulo else self.activo.codigo


class HistorialSolicitud(BaseModel):
    """
    Modelo para el historial de cambios de estado de solicitudes.

    Registra cada cambio de estado que experimenta una solicitud, permitiendo
    trazabilidad completa del proceso de aprobación y despacho.

    Attributes:
        solicitud: Solicitud a la que pertenece el registro.
        estado_anterior: Estado previo al cambio (opcional para el primer estado).
        estado_nuevo: Estado resultante del cambio.
        usuario: Usuario que realizó el cambio de estado.
        observaciones: Observaciones sobre el cambio de estado (opcional).
        fecha_cambio: Fecha y hora del cambio de estado.
    """

    solicitud = models.ForeignKey(
        Solicitud,
        on_delete=models.CASCADE,
        related_name='historial',
        verbose_name='Solicitud',
        help_text='Solicitud a la que pertenece el registro'
    )
    estado_anterior = models.ForeignKey(
        EstadoSolicitud,
        on_delete=models.PROTECT,
        related_name='historiales_anterior',
        verbose_name='Estado Anterior',
        blank=True,
        null=True,
        help_text='Estado previo al cambio'
    )
    estado_nuevo = models.ForeignKey(
        EstadoSolicitud,
        on_delete=models.PROTECT,
        related_name='historiales_nuevo',
        verbose_name='Estado Nuevo',
        help_text='Estado resultante del cambio'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='cambios_estado_solicitud',
        verbose_name='Usuario',
        help_text='Usuario que realizó el cambio de estado'
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones',
        help_text='Observaciones sobre el cambio de estado'
    )
    fecha_cambio = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Cambio',
        help_text='Fecha y hora del cambio de estado'
    )

    class Meta:
        db_table = 'tba_solicitudes_historial'
        verbose_name = 'Historial de Solicitud'
        verbose_name_plural = 'Historial de Solicitudes'
        ordering = ['-fecha_cambio']
        indexes = [
            models.Index(fields=['solicitud']),
            models.Index(fields=['fecha_cambio']),
            models.Index(fields=['usuario']),
        ]

    def __str__(self) -> str:
        """Representación en cadena del registro de historial."""
        return f"{self.solicitud.numero} - {self.estado_nuevo.nombre} ({self.fecha_cambio})"

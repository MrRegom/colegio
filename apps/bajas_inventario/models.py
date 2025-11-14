"""
Modelos del módulo de bajas de inventario.

Este módulo gestiona las bajas de activos del inventario, incluyendo:
- Catálogo de motivos de baja
- Registro de bajas de inventario con trazabilidad completa

Todos los modelos heredan de BaseModel para mantener auditoría y soft delete.
Convención de nomenclatura: todas las tablas tienen prefijo 'tba_'.
"""
from __future__ import annotations

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

from core.models import BaseModel
from apps.activos.models import Activo, Ubicacion


class MotivoBaja(BaseModel):
    """
    Catálogo de motivos de baja de inventario.

    Define las razones por las cuales un activo puede ser dado de baja
    (obsolescencia, daño irreparable, robo, etc.).
    Hereda de BaseModel para soft delete y auditoría.
    """
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tba_baja_motivo'
        verbose_name = 'Motivo de Baja'
        verbose_name_plural = 'Motivos de Baja'
        ordering = ['codigo']

    def __str__(self) -> str:
        """Representación en string del objeto."""
        return f"{self.codigo} - {self.nombre}"


class BajaInventario(BaseModel):
    """
    Modelo para gestionar bajas de inventario.

    Registra la baja de activos del inventario con toda la información
    de trazabilidad: motivo, fecha, ubicación, solicitante, etc.
    Hereda de BaseModel para soft delete y auditoría.
    """
    activo = models.ForeignKey(
        Activo,
        on_delete=models.PROTECT,
        related_name='detalles_baja',
        verbose_name='Activo'
    )
    numero = models.CharField(max_length=20, unique=True, verbose_name='Número de Baja')
    fecha_baja = models.DateField(verbose_name='Fecha de Baja')
    motivo = models.ForeignKey(
        MotivoBaja,
        on_delete=models.PROTECT,
        related_name='bajas',
        verbose_name='Motivo'
    )
    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name='bajas_inventario',
        verbose_name='Ubicación de Baja'
    )
    solicitante = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='bajas_solicitadas',
        verbose_name='Solicitante'
    )
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    class Meta:
        db_table = 'tba_baja_inventario'
        verbose_name = 'Baja de Inventario'
        verbose_name_plural = 'Bajas de Inventario'
        ordering = ['-fecha_baja', '-numero']
        permissions = [
            ('registrar_baja', 'Puede registrar bajas de inventario'),
            ('aprobar_baja', 'Puede aprobar bajas de inventario'),
            ('ver_reportes_bajas', 'Puede ver reportes de bajas'),
        ]

    def __str__(self) -> str:
        """Representación en string del objeto."""
        return f"BAJA-{self.numero} - {self.motivo.nombre}"

"""
Utilidades de lógica de negocio reutilizables.

Contiene funciones para validación de RUT, generación de códigos,
formateo de texto y otras utilidades de negocio.
"""
from typing import Optional
import re


def format_rut(rut: str) -> str:
    """
    Formatea un RUT chileno al formato estándar XX.XXX.XXX-X.

    Args:
        rut: RUT sin formato (ej: '12345678-9' o '123456789')

    Returns:
        str: RUT formateado (ej: '12.345.678-9')

    Example:
        >>> format_rut('123456789')
        '12.345.678-9'
    """
    # Limpiar RUT: remover puntos, guiones y espacios
    rut_limpio: str = rut.replace('.', '').replace('-', '').replace(' ', '').upper()

    if not rut_limpio:
        return ''

    # Separar número y dígito verificador
    if len(rut_limpio) < 2:
        return rut_limpio

    numero: str = rut_limpio[:-1]
    dv: str = rut_limpio[-1]

    # Formatear con puntos de miles
    numero_formateado: str = ''
    contador: int = 0

    for digito in reversed(numero):
        if contador > 0 and contador % 3 == 0:
            numero_formateado = f'.{numero_formateado}'
        numero_formateado = f'{digito}{numero_formateado}'
        contador += 1

    return f'{numero_formateado}-{dv}'


def validar_rut(rut: str) -> bool:
    """
    Valida un RUT chileno usando el algoritmo del módulo 11.

    Args:
        rut: RUT a validar (puede tener formato o no)

    Returns:
        bool: True si el RUT es válido, False en caso contrario

    Example:
        >>> validar_rut('12.345.678-9')
        True
        >>> validar_rut('12345678-9')
        True
        >>> validar_rut('12345678-0')
        False
    """
    # Limpiar RUT
    rut_limpio: str = rut.replace('.', '').replace('-', '').replace(' ', '').upper()

    if len(rut_limpio) < 2:
        return False

    # Separar número y dígito verificador
    numero_str: str = rut_limpio[:-1]
    dv_ingresado: str = rut_limpio[-1]

    # Validar que el número sea numérico
    if not numero_str.isdigit():
        return False

    # Calcular dígito verificador
    numero: int = int(numero_str)
    suma: int = 0
    multiplicador: int = 2

    while numero > 0:
        suma += (numero % 10) * multiplicador
        numero //= 10
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2

    resto: int = suma % 11
    dv_calculado: str = str(11 - resto)

    # Casos especiales
    if dv_calculado == '11':
        dv_calculado = '0'
    elif dv_calculado == '10':
        dv_calculado = 'K'

    return dv_ingresado == dv_calculado


def truncar_texto(texto: str, longitud: int = 100, sufijo: str = '...') -> str:
    """
    Trunca un texto a una longitud máxima agregando un sufijo.

    Args:
        texto: Texto a truncar
        longitud: Longitud máxima (default: 100)
        sufijo: Sufijo a agregar si se trunca (default: '...')

    Returns:
        str: Texto truncado con sufijo si corresponde

    Example:
        >>> truncar_texto('Este es un texto muy largo', 10)
        'Este es...'
    """
    if not texto:
        return ''

    if len(texto) <= longitud:
        return texto

    return texto[:longitud - len(sufijo)].strip() + sufijo


def generar_codigo_unico(
    prefijo: str,
    modelo,
    campo: str = 'codigo',
    longitud: int = 6
) -> str:
    """
    Genera un código único para un modelo usando un prefijo.

    Args:
        prefijo: Prefijo del código (ej: 'ART', 'CAT', 'MOV')
        modelo: Clase del modelo Django
        campo: Nombre del campo que contiene el código (default: 'codigo')
        longitud: Longitud del número secuencial (default: 6)

    Returns:
        str: Código único generado (ej: 'ART-000001')

    Example:
        >>> from apps.bodega.models import Articulo
        >>> codigo = generar_codigo_unico('ART', Articulo)
        >>> codigo
        'ART-000001'
    """
    # Buscar el último código con ese prefijo
    ultimos = modelo.objects.filter(
        **{f'{campo}__startswith': f'{prefijo}-'}
    ).order_by(f'-{campo}')[:1]

    if ultimos.exists():
        ultimo_codigo: str = getattr(ultimos[0], campo)
        # Extraer el número del código
        match = re.search(r'(\d+)$', ultimo_codigo)
        if match:
            ultimo_numero: int = int(match.group(1))
            nuevo_numero: int = ultimo_numero + 1
        else:
            nuevo_numero = 1
    else:
        nuevo_numero = 1

    # Formatear con ceros a la izquierda
    return f'{prefijo}-{nuevo_numero:0{longitud}d}'


def generar_codigo_con_anio(
    prefijo: str,
    modelo,
    campo: str = 'numero',
    longitud: int = 6
) -> str:
    """
    Genera un código único para un modelo usando un prefijo y el año actual.
    El correlativo se reinicia cada año.

    Args:
        prefijo: Prefijo del código (ej: 'OC', 'SOL', 'FAC')
        modelo: Clase del modelo Django
        campo: Nombre del campo que contiene el código (default: 'numero')
        longitud: Longitud del número secuencial (default: 6)

    Returns:
        str: Código único generado (ej: 'OC-2025-000001')

    Example:
        >>> from apps.compras.models import OrdenCompra
        >>> codigo = generar_codigo_con_anio('OC', OrdenCompra)
        >>> codigo
        'OC-2025-000001'
    """
    from datetime import datetime

    # Obtener el año actual
    anio_actual: int = datetime.now().year

    # Buscar el último código con ese prefijo y año
    patron_busqueda: str = f'{prefijo}-{anio_actual}-'
    ultimos = modelo.objects.filter(
        **{f'{campo}__startswith': patron_busqueda}
    ).order_by(f'-{campo}')[:1]

    if ultimos.exists():
        ultimo_codigo: str = getattr(ultimos[0], campo)
        # Extraer el número del código (después del segundo guion)
        match = re.search(r'(\d+)$', ultimo_codigo)
        if match:
            ultimo_numero: int = int(match.group(1))
            nuevo_numero: int = ultimo_numero + 1
        else:
            nuevo_numero = 1
    else:
        nuevo_numero = 1

    # Formatear con ceros a la izquierda
    return f'{prefijo}-{anio_actual}-{nuevo_numero:0{longitud}d}'

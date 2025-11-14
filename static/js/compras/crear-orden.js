/**
 * Funcionalidad para crear órdenes de compra desde solicitudes
 * @module compras/crear-orden
 * @description Carga automáticamente los artículos de solicitudes seleccionadas
 */

(function() {
    'use strict';

    /**
     * Inicializa la funcionalidad de carga de artículos
     */
    function inicializarCargaArticulos() {
        const selectSolicitudes = document.getElementById('id_solicitudes');
        const previewContainer = document.getElementById('preview-articulos');

        if (!selectSolicitudes || !previewContainer) {
            return;
        }

        // Cargar artículos cuando cambien las solicitudes seleccionadas
        selectSolicitudes.addEventListener('change', function() {
            cargarArticulosDeSolicitudes();
        });
    }

    /**
     * Carga los artículos de las solicitudes seleccionadas vía AJAX
     */
    function cargarArticulosDeSolicitudes() {
        const selectSolicitudes = document.getElementById('id_solicitudes');
        const previewContainer = document.getElementById('preview-articulos');
        const selectedOptions = Array.from(selectSolicitudes.selectedOptions);
        const solicitudIds = selectedOptions.map(option => option.value);

        // Si no hay solicitudes seleccionadas, limpiar preview
        if (solicitudIds.length === 0) {
            previewContainer.innerHTML = '';
            previewContainer.classList.add('d-none');
            return;
        }

        // Mostrar loading
        previewContainer.innerHTML = '<div class="text-center p-3"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div></div>';
        previewContainer.classList.remove('d-none');

        // Construir URL con parámetros
        const params = new URLSearchParams();
        solicitudIds.forEach(id => params.append('solicitudes[]', id));

        // Obtener URL desde data attribute o construirla
        const url = selectSolicitudes.getAttribute('data-url-detalles') || '/compras/api/obtener-detalles-solicitudes/';

        // Hacer petición AJAX
        fetch(`${url}?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                mostrarPreviewArticulos(data.detalles);
            })
            .catch(error => {
                console.error('Error al cargar artículos:', error);
                previewContainer.innerHTML = '<div class="alert alert-danger">Error al cargar los artículos</div>';
            });
    }

    /**
     * Muestra el preview de los artículos que se agregarán a la orden
     * @param {Array} detalles - Array de detalles de solicitudes
     */
    function mostrarPreviewArticulos(detalles) {
        const previewContainer = document.getElementById('preview-articulos');

        if (detalles.length === 0) {
            previewContainer.innerHTML = '<div class="alert alert-info">Las solicitudes seleccionadas no tienen artículos aprobados</div>';
            return;
        }

        // Construir tabla HTML
        let html = `
            <div class="card mt-3">
                <div class="card-header bg-light">
                    <h5 class="card-title mb-0">
                        <i class="ri-file-list-line"></i> Artículos que se agregarán automáticamente
                    </h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-sm table-hover mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th>Solicitud</th>
                                    <th>Tipo</th>
                                    <th>Código</th>
                                    <th>Producto</th>
                                    <th class="text-end">Cantidad</th>
                                    <th class="text-end">Precio Unit.</th>
                                </tr>
                            </thead>
                            <tbody>
        `;

        detalles.forEach(detalle => {
            const tipoBadge = detalle.tipo === 'articulo'
                ? '<span class="badge bg-primary">Artículo</span>'
                : '<span class="badge bg-info">Activo</span>';

            html += `
                <tr>
                    <td><small class="text-muted">${detalle.solicitud_numero}</small></td>
                    <td>${tipoBadge}</td>
                    <td><code>${detalle.codigo}</code></td>
                    <td>${detalle.nombre}</td>
                    <td class="text-end"><strong>${detalle.cantidad_aprobada}</strong> ${detalle.unidad_medida}</td>
                    <td class="text-end">$${formatearNumero(detalle.precio_unitario)}</td>
                </tr>
            `;
        });

        html += `
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="card-footer bg-light">
                    <div class="alert alert-success mb-0">
                        <i class="ri-information-line"></i>
                        <strong>${detalles.length}</strong> artículo(s) se agregarán automáticamente al crear la orden de compra.
                    </div>
                </div>
            </div>
        `;

        previewContainer.innerHTML = html;
    }

    /**
     * Formatea un número con separadores de miles
     * @param {string|number} numero - Número a formatear
     * @returns {string} - Número formateado
     */
    function formatearNumero(numero) {
        const num = parseFloat(numero);
        if (isNaN(num)) return '0';
        return num.toLocaleString('es-CL', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 2
        });
    }

    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', inicializarCargaArticulos);
    } else {
        inicializarCargaArticulos();
    }

})();

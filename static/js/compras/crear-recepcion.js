/**
 * Funcionalidad para crear recepciones de artículos
 * @module compras/crear-recepcion
 * @description Maneja la selección dinámica de artículos, cantidades y validaciones
 */

(function() {
    'use strict';

    // Variables globales
    let articulosSeleccionados = [];
    let modalArticulo;
    let contadorFilas = 0;

    /**
     * Inicializa la funcionalidad del formulario de recepción
     */
    function inicializar() {
        // Inicializar modal de Bootstrap
        const modalElement = document.getElementById('modalArticulo');
        if (modalElement) {
            modalArticulo = new bootstrap.Modal(modalElement);
        }

        // Event listeners
        setupEventListeners();

        // Mostrar/ocultar orden de compra según tipo
        manejarCambioTipo();

        // Actualizar visualización inicial
        actualizarVisualizacionArticulos();
    }

    /**
     * Configura todos los event listeners
     */
    function setupEventListeners() {
        // Botón para abrir modal de agregar artículo
        const btnAgregar = document.getElementById('btn-agregar-articulo');
        if (btnAgregar) {
            btnAgregar.addEventListener('click', () => {
                modalArticulo.show();
            });
        }

        // Buscador de artículos en el modal
        const inputBuscar = document.getElementById('buscar-articulo');
        if (inputBuscar) {
            inputBuscar.addEventListener('input', filtrarArticulos);
        }

        // Botones de selección de artículos en el modal
        document.querySelectorAll('.btn-seleccionar-articulo').forEach(btn => {
            btn.addEventListener('click', seleccionarArticulo);
        });

        // Cambio de tipo de recepción
        const selectTipo = document.getElementById('id_tipo');
        if (selectTipo) {
            selectTipo.addEventListener('change', manejarCambioTipo);
        }

        // Cambio de orden de compra
        const selectOrdenCompra = document.getElementById('id_orden_compra');
        if (selectOrdenCompra) {
            selectOrdenCompra.addEventListener('change', cargarArticulosDeOrden);
        }

        // Submit del formulario
        const form = document.getElementById('formRecepcion');
        if (form) {
            form.addEventListener('submit', validarYEnviarFormulario);
        }
    }

    /**
     * Maneja el cambio de tipo de recepción
     * Muestra/oculta el campo de orden de compra según si el tipo lo requiere
     */
    function manejarCambioTipo() {
        const selectTipo = document.getElementById('id_tipo');
        const ordenCompraWrapper = document.getElementById('orden_compra_wrapper');
        const ordenCompraSelect = document.getElementById('id_orden_compra');
        const ordenRequired = document.querySelector('.orden-required');

        if (!selectTipo || !tiposRecepcion) return;

        const tipoId = selectTipo.value;

        // Buscar el tipo seleccionado
        const tipoSeleccionado = tiposRecepcion.find(t => t.id == tipoId);

        if (tipoSeleccionado && tipoSeleccionado.requiere_orden) {
            // Mostrar y hacer requerido el campo de orden de compra
            if (ordenCompraWrapper) {
                ordenCompraWrapper.classList.remove('d-none');
            }
            if (ordenCompraSelect) {
                ordenCompraSelect.required = true;
            }
            if (ordenRequired) {
                ordenRequired.classList.remove('d-none');
            }
        } else {
            // Ocultar y quitar requerimiento del campo de orden de compra
            if (ordenCompraWrapper) {
                ordenCompraWrapper.classList.add('d-none');
            }
            if (ordenCompraSelect) {
                ordenCompraSelect.required = false;
                ordenCompraSelect.value = '';
            }
            if (ordenRequired) {
                ordenRequired.classList.add('d-none');
            }
        }
    }

    /**
     * Carga automáticamente los artículos de la orden de compra seleccionada
     */
    function cargarArticulosDeOrden() {
        const selectOrdenCompra = document.getElementById('id_orden_compra');
        const ordenId = selectOrdenCompra.value;

        if (!ordenId) {
            // Si no hay orden seleccionada, limpiar artículos
            limpiarArticulos();
            return;
        }

        // Mostrar loading
        mostrarAlerta('Cargando artículos de la orden de compra...', 'info');

        // Hacer petición AJAX
        fetch(`${urlObtenerArticulosOC}?orden_id=${ordenId}`)
            .then(response => response.json())
            .then(data => {
                if (data.articulos && data.articulos.length > 0) {
                    // Limpiar artículos actuales
                    limpiarArticulos();

                    // Agregar cada artículo de la orden
                    data.articulos.forEach(articulo => {
                        // Verificar si no está ya agregado
                        if (!articulosSeleccionados.some(a => a.id === articulo.id && a.tipo === articulo.tipo)) {
                            // Agregar a la lista
                            const articuloData = {
                                id: articulo.id,
                                codigo: articulo.codigo,
                                nombre: articulo.nombre,
                                unidad: articulo.unidad_medida,
                                tipo: articulo.tipo
                            };

                            articulosSeleccionados.push(articuloData);
                            agregarFilaArticuloConCantidad(articuloData, articulo.cantidad);
                        }
                    });

                    actualizarVisualizacionArticulos();
                    mostrarAlerta(`${data.articulos.length} artículo(s) cargados de la orden de compra`, 'success');
                } else {
                    mostrarAlerta('La orden de compra no tiene artículos asociados', 'warning');
                }
            })
            .catch(error => {
                console.error('Error al cargar artículos:', error);
                mostrarAlerta('Error al cargar los artículos de la orden', 'danger');
            });
    }

    /**
     * Limpia todos los artículos de la tabla
     */
    function limpiarArticulos() {
        articulosSeleccionados = [];
        const tbody = document.getElementById('tbody-articulos');
        tbody.innerHTML = '';
        actualizarVisualizacionArticulos();
    }

    /**
     * Filtra la lista de artículos en el modal según el término de búsqueda
     * @param {Event} e - Evento input
     */
    function filtrarArticulos(e) {
        const termino = e.target.value.toLowerCase();
        const filas = document.querySelectorAll('#tbody-lista-articulos tr');

        filas.forEach(fila => {
            const sku = fila.dataset.articuloSku.toLowerCase();
            const codigo = fila.dataset.articuloCodigo.toLowerCase();
            const nombre = fila.dataset.articuloNombre.toLowerCase();

            if (sku.includes(termino) || codigo.includes(termino) || nombre.includes(termino)) {
                fila.style.display = '';
            } else {
                fila.style.display = 'none';
            }
        });
    }

    /**
     * Selecciona un artículo y lo agrega a la tabla
     * @param {Event} e - Evento click
     */
    function seleccionarArticulo(e) {
        const fila = e.target.closest('tr');
        const articuloId = parseInt(fila.dataset.articuloId);

        // Verificar si el artículo ya está seleccionado (tipo articulo por defecto desde el modal)
        if (articulosSeleccionados.some(a => a.id === articuloId && a.tipo === 'articulo')) {
            mostrarAlerta('Este artículo ya ha sido agregado', 'warning');
            return;
        }

        // Agregar artículo a la lista
        const articulo = {
            id: articuloId,
            sku: fila.dataset.articuloSku,
            codigo: fila.dataset.articuloCodigo,
            nombre: fila.dataset.articuloNombre,
            unidad: fila.dataset.articuloUnidad,
            tipo: 'articulo'
        };

        articulosSeleccionados.push(articulo);
        agregarFilaArticulo(articulo);

        // Cerrar modal
        modalArticulo.hide();

        // Limpiar búsqueda
        document.getElementById('buscar-articulo').value = '';
        document.querySelectorAll('#tbody-lista-articulos tr').forEach(tr => {
            tr.style.display = '';
        });

        // Actualizar visualización
        actualizarVisualizacionArticulos();
    }

    /**
     * Agrega una fila de artículo a la tabla
     * @param {Object} articulo - Datos del artículo
     */
    function agregarFilaArticulo(articulo) {
        const tbody = document.getElementById('tbody-articulos');
        const fila = document.createElement('tr');
        fila.dataset.articuloId = articulo.id;
        fila.dataset.filaId = contadorFilas;
        fila.dataset.tipo = articulo.tipo || 'articulo';

        fila.innerHTML = `
            <td>
                <strong>${articulo.nombre}</strong><br>
                <small class="text-muted">Código: ${articulo.codigo}</small>
                <input type="hidden" name="detalles[${contadorFilas}][articulo_id]" value="${articulo.id}">
            </td>
            <td>
                <input type="number"
                       name="detalles[${contadorFilas}][cantidad]"
                       class="form-control form-control-sm"
                       min="0.01"
                       step="0.01"
                       required
                       placeholder="0.00">
                <small class="text-muted">${articulo.unidad}</small>
            </td>
            <td>
                <input type="text"
                       name="detalles[${contadorFilas}][lote]"
                       class="form-control form-control-sm"
                       placeholder="Opcional">
            </td>
            <td>
                <input type="date"
                       name="detalles[${contadorFilas}][fecha_vencimiento]"
                       class="form-control form-control-sm">
            </td>
            <td>
                <input type="text"
                       name="detalles[${contadorFilas}][observaciones]"
                       class="form-control form-control-sm"
                       placeholder="Opcional">
            </td>
            <td class="text-center">
                <button type="button" class="btn btn-sm btn-danger btn-eliminar-fila" data-fila-id="${contadorFilas}">
                    <i class="ri-delete-bin-line"></i>
                </button>
            </td>
        `;

        tbody.appendChild(fila);

        // Event listener para eliminar fila
        fila.querySelector('.btn-eliminar-fila').addEventListener('click', eliminarFilaArticulo);

        contadorFilas++;
    }

    /**
     * Agrega una fila de artículo a la tabla con cantidad prellenada
     * @param {Object} articulo - Datos del artículo
     * @param {string} cantidad - Cantidad a prellenar
     */
    function agregarFilaArticuloConCantidad(articulo, cantidad) {
        const tbody = document.getElementById('tbody-articulos');
        const fila = document.createElement('tr');
        fila.dataset.articuloId = articulo.id;
        fila.dataset.filaId = contadorFilas;
        fila.dataset.tipo = articulo.tipo || 'articulo';

        fila.innerHTML = `
            <td>
                <strong>${articulo.nombre}</strong><br>
                <small class="text-muted">Código: ${articulo.codigo}</small>
                <input type="hidden" name="detalles[${contadorFilas}][articulo_id]" value="${articulo.id}">
            </td>
            <td>
                <input type="number"
                       name="detalles[${contadorFilas}][cantidad]"
                       class="form-control form-control-sm"
                       min="0.01"
                       step="0.01"
                       value="${cantidad}"
                       required
                       placeholder="0.00">
                <small class="text-muted">${articulo.unidad}</small>
            </td>
            <td>
                <input type="text"
                       name="detalles[${contadorFilas}][lote]"
                       class="form-control form-control-sm"
                       placeholder="Opcional">
            </td>
            <td>
                <input type="date"
                       name="detalles[${contadorFilas}][fecha_vencimiento]"
                       class="form-control form-control-sm">
            </td>
            <td>
                <input type="text"
                       name="detalles[${contadorFilas}][observaciones]"
                       class="form-control form-control-sm"
                       placeholder="Opcional">
            </td>
            <td class="text-center">
                <button type="button" class="btn btn-sm btn-danger btn-eliminar-fila" data-fila-id="${contadorFilas}">
                    <i class="ri-delete-bin-line"></i>
                </button>
            </td>
        `;

        tbody.appendChild(fila);

        // Event listener para eliminar fila
        fila.querySelector('.btn-eliminar-fila').addEventListener('click', eliminarFilaArticulo);

        contadorFilas++;
    }

    /**
     * Elimina una fila de artículo
     * @param {Event} e - Evento click
     */
    function eliminarFilaArticulo(e) {
        const filaId = e.target.closest('button').dataset.filaId;
        const fila = document.querySelector(`tr[data-fila-id="${filaId}"]`);
        const articuloId = parseInt(fila.dataset.articuloId);
        const tipo = fila.dataset.tipo || 'articulo';

        // Remover de la lista de seleccionados (comparar id y tipo)
        articulosSeleccionados = articulosSeleccionados.filter(a => !(a.id === articuloId && a.tipo === tipo));

        // Remover del DOM
        fila.remove();

        // Actualizar visualización
        actualizarVisualizacionArticulos();
    }

    /**
     * Actualiza la visualización de artículos (muestra/oculta mensaje de vacío)
     */
    function actualizarVisualizacionArticulos() {
        const tbody = document.getElementById('tbody-articulos');
        const sinArticulos = document.getElementById('sin-articulos');
        const tabla = document.getElementById('tabla-articulos');

        if (articulosSeleccionados.length === 0) {
            tabla.style.display = 'none';
            sinArticulos.style.display = 'block';
        } else {
            tabla.style.display = 'table';
            sinArticulos.style.display = 'none';
        }
    }

    /**
     * Valida y envía el formulario
     * @param {Event} e - Evento submit
     */
    function validarYEnviarFormulario(e) {
        // Validar que haya al menos un artículo
        if (articulosSeleccionados.length === 0) {
            e.preventDefault();
            mostrarAlerta('Debe agregar al menos un artículo a la recepción', 'warning');
            return false;
        }

        // Validar cantidades
        const inputsCantidad = document.querySelectorAll('input[name^="detalles"][name$="[cantidad]"]');
        let todasValidas = true;

        inputsCantidad.forEach(input => {
            const valor = parseFloat(input.value);
            if (!valor || valor <= 0) {
                todasValidas = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });

        if (!todasValidas) {
            e.preventDefault();
            mostrarAlerta('Todas las cantidades deben ser mayores a cero', 'warning');
            return false;
        }

        // Si todo está bien, permitir envío
        return true;
    }

    /**
     * Muestra una alerta temporal
     * @param {string} mensaje - Mensaje a mostrar
     * @param {string} tipo - Tipo de alerta (success, warning, danger, info)
     */
    function mostrarAlerta(mensaje, tipo = 'info') {
        const alerta = document.createElement('div');
        alerta.className = `alert alert-${tipo} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
        alerta.style.zIndex = '9999';
        alerta.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        document.body.appendChild(alerta);

        // Auto-cerrar después de 5 segundos
        setTimeout(() => {
            alerta.remove();
        }, 5000);
    }

    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', inicializar);
    } else {
        inicializar();
    }

})();

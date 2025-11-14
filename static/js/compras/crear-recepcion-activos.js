/**
 * Funcionalidad para crear recepciones de bienes/activos
 * @module compras/crear-recepcion-activos
 * @description Maneja la selección dinámica de activos, cantidades y validaciones
 */

(function() {
    'use strict';

    // Variables globales
    let activosSeleccionados = [];
    let modalActivo;
    let contadorFilas = 0;

    /**
     * Inicializa la funcionalidad del formulario de recepción
     */
    function inicializar() {
        // Inicializar modal de Bootstrap
        const modalElement = document.getElementById('modalActivo');
        if (modalElement) {
            modalActivo = new bootstrap.Modal(modalElement);
        }

        // Event listeners
        setupEventListeners();

        // Mostrar/ocultar orden de compra según tipo
        manejarCambioTipo();

        // Actualizar visualización inicial
        actualizarVisualizacionActivos();
    }

    /**
     * Configura todos los event listeners
     */
    function setupEventListeners() {
        // Botón para abrir modal de agregar activo
        const btnAgregar = document.getElementById('btn-agregar-activo');
        if (btnAgregar) {
            btnAgregar.addEventListener('click', () => {
                modalActivo.show();
            });
        }

        // Buscador de activos en el modal
        const inputBuscar = document.getElementById('buscar-activo');
        if (inputBuscar) {
            inputBuscar.addEventListener('input', filtrarActivos);
        }

        // Botones de selección de activos en el modal
        document.querySelectorAll('.btn-seleccionar-activo').forEach(btn => {
            btn.addEventListener('click', seleccionarActivo);
        });

        // Cambio de tipo de recepción
        const selectTipo = document.getElementById('id_tipo');
        if (selectTipo) {
            selectTipo.addEventListener('change', manejarCambioTipo);
        }

        // Cambio de orden de compra
        const selectOrdenCompra = document.getElementById('id_orden_compra');
        if (selectOrdenCompra) {
            selectOrdenCompra.addEventListener('change', cargarActivosDeOrden);
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
     * Carga automáticamente los activos de la orden de compra seleccionada
     */
    function cargarActivosDeOrden() {
        const selectOrdenCompra = document.getElementById('id_orden_compra');
        const ordenId = selectOrdenCompra.value;

        if (!ordenId) {
            // Si no hay orden seleccionada, limpiar activos
            limpiarActivos();
            return;
        }

        // Mostrar loading
        mostrarAlerta('Cargando bienes/activos de la orden de compra...', 'info');

        // Hacer petición AJAX
        fetch(`${urlObtenerActivosOC}?orden_id=${ordenId}`)
            .then(response => response.json())
            .then(data => {
                if (data.activos && data.activos.length > 0) {
                    // Limpiar activos actuales
                    limpiarActivos();

                    // Agregar cada activo de la orden
                    data.activos.forEach(activo => {
                        // Verificar si no está ya agregado
                        if (!activosSeleccionados.some(a => a.id === activo.id)) {
                            // Agregar a la lista
                            const activoData = {
                                id: activo.id,
                                codigo: activo.codigo,
                                nombre: activo.nombre,
                                requiere_serie: activo.requiere_serie
                            };

                            activosSeleccionados.push(activoData);
                            agregarFilaActivoConCantidad(activoData, activo.cantidad);
                        }
                    });

                    actualizarVisualizacionActivos();
                    mostrarAlerta(`${data.activos.length} bien(es)/activo(s) cargados de la orden de compra`, 'success');
                } else {
                    mostrarAlerta('La orden de compra no tiene bienes/activos asociados', 'warning');
                }
            })
            .catch(error => {
                console.error('Error al cargar activos:', error);
                mostrarAlerta('Error al cargar los bienes/activos de la orden', 'danger');
            });
    }

    /**
     * Limpia todos los activos de la tabla
     */
    function limpiarActivos() {
        activosSeleccionados = [];
        const tbody = document.getElementById('tbody-activos');
        tbody.innerHTML = '';
        actualizarVisualizacionActivos();
    }

    /**
     * Filtra la lista de activos en el modal según el término de búsqueda
     * @param {Event} e - Evento input
     */
    function filtrarActivos(e) {
        const termino = e.target.value.toLowerCase();
        const filas = document.querySelectorAll('#tbody-lista-activos tr');

        filas.forEach(fila => {
            const codigo = fila.dataset.activoCodigo.toLowerCase();
            const nombre = fila.dataset.activoNombre.toLowerCase();

            if (codigo.includes(termino) || nombre.includes(termino)) {
                fila.style.display = '';
            } else {
                fila.style.display = 'none';
            }
        });
    }

    /**
     * Selecciona un activo y lo agrega a la tabla
     * @param {Event} e - Evento click
     */
    function seleccionarActivo(e) {
        const fila = e.target.closest('tr');
        const activoId = parseInt(fila.dataset.activoId);

        // Verificar si el activo ya está seleccionado
        if (activosSeleccionados.some(a => a.id === activoId)) {
            mostrarAlerta('Este bien/activo ya ha sido agregado', 'warning');
            return;
        }

        // Agregar activo a la lista
        const activo = {
            id: activoId,
            codigo: fila.dataset.activoCodigo,
            nombre: fila.dataset.activoNombre,
            requiere_serie: fila.dataset.activoRequiereSerie === 'True'
        };

        activosSeleccionados.push(activo);
        agregarFilaActivo(activo);

        // Cerrar modal
        modalActivo.hide();

        // Limpiar búsqueda
        document.getElementById('buscar-activo').value = '';
        document.querySelectorAll('#tbody-lista-activos tr').forEach(tr => {
            tr.style.display = '';
        });

        // Actualizar visualización
        actualizarVisualizacionActivos();
    }

    /**
     * Agrega una fila de activo a la tabla
     * @param {Object} activo - Datos del activo
     */
    function agregarFilaActivo(activo) {
        const tbody = document.getElementById('tbody-activos');
        const fila = document.createElement('tr');
        fila.dataset.activoId = activo.id;
        fila.dataset.filaId = contadorFilas;

        const requiereSerieClass = activo.requiere_serie ? 'border-warning' : '';
        const requiereSerieRequired = activo.requiere_serie ? 'required' : '';

        fila.innerHTML = `
            <td>
                <strong>${activo.nombre}</strong><br>
                <small class="text-muted">Código: ${activo.codigo}</small>
                <input type="hidden" name="detalles[${contadorFilas}][activo_id]" value="${activo.id}">
            </td>
            <td>
                <input type="number"
                       name="detalles[${contadorFilas}][cantidad]"
                       class="form-control form-control-sm"
                       min="1"
                       step="1"
                       required
                       placeholder="0">
            </td>
            <td>
                <input type="text"
                       name="detalles[${contadorFilas}][numero_serie]"
                       class="form-control form-control-sm ${requiereSerieClass}"
                       ${requiereSerieRequired}
                       placeholder="${activo.requiere_serie ? 'Requerido' : 'Opcional'}">
                ${activo.requiere_serie ? '<small class="text-warning">Requerido</small>' : ''}
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
        fila.querySelector('.btn-eliminar-fila').addEventListener('click', eliminarFilaActivo);

        contadorFilas++;
    }

    /**
     * Agrega una fila de activo a la tabla con cantidad prellenada
     * @param {Object} activo - Datos del activo
     * @param {string} cantidad - Cantidad a prellenar
     */
    function agregarFilaActivoConCantidad(activo, cantidad) {
        const tbody = document.getElementById('tbody-activos');
        const fila = document.createElement('tr');
        fila.dataset.activoId = activo.id;
        fila.dataset.filaId = contadorFilas;

        const requiereSerieClass = activo.requiere_serie ? 'border-warning' : '';
        const requiereSerieRequired = activo.requiere_serie ? 'required' : '';

        fila.innerHTML = `
            <td>
                <strong>${activo.nombre}</strong><br>
                <small class="text-muted">Código: ${activo.codigo}</small>
                <input type="hidden" name="detalles[${contadorFilas}][activo_id]" value="${activo.id}">
            </td>
            <td>
                <input type="number"
                       name="detalles[${contadorFilas}][cantidad]"
                       class="form-control form-control-sm"
                       min="1"
                       step="1"
                       value="${cantidad}"
                       required
                       placeholder="0">
            </td>
            <td>
                <input type="text"
                       name="detalles[${contadorFilas}][numero_serie]"
                       class="form-control form-control-sm ${requiereSerieClass}"
                       ${requiereSerieRequired}
                       placeholder="${activo.requiere_serie ? 'Requerido' : 'Opcional'}">
                ${activo.requiere_serie ? '<small class="text-warning">Requerido</small>' : ''}
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
        fila.querySelector('.btn-eliminar-fila').addEventListener('click', eliminarFilaActivo);

        contadorFilas++;
    }

    /**
     * Elimina una fila de activo
     * @param {Event} e - Evento click
     */
    function eliminarFilaActivo(e) {
        const filaId = e.target.closest('button').dataset.filaId;
        const fila = document.querySelector(`tr[data-fila-id="${filaId}"]`);
        const activoId = parseInt(fila.dataset.activoId);

        // Remover de la lista de seleccionados
        activosSeleccionados = activosSeleccionados.filter(a => a.id !== activoId);

        // Remover del DOM
        fila.remove();

        // Actualizar visualización
        actualizarVisualizacionActivos();
    }

    /**
     * Actualiza la visualización de activos (muestra/oculta mensaje de vacío)
     */
    function actualizarVisualizacionActivos() {
        const tbody = document.getElementById('tbody-activos');
        const sinActivos = document.getElementById('sin-activos');
        const tabla = document.getElementById('tabla-activos');

        if (activosSeleccionados.length === 0) {
            tabla.style.display = 'none';
            sinActivos.style.display = 'block';
        } else {
            tabla.style.display = 'table';
            sinActivos.style.display = 'none';
        }
    }

    /**
     * Valida y envía el formulario
     * @param {Event} e - Evento submit
     */
    function validarYEnviarFormulario(e) {
        // Validar que haya al menos un activo
        if (activosSeleccionados.length === 0) {
            e.preventDefault();
            mostrarAlerta('Debe agregar al menos un bien/activo a la recepción', 'warning');
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

        // Validar números de serie requeridos
        const inputsSerie = document.querySelectorAll('input[name^="detalles"][name$="[numero_serie]"][required]');
        let todasSeriesValidas = true;

        inputsSerie.forEach(input => {
            if (!input.value.trim()) {
                todasSeriesValidas = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });

        if (!todasSeriesValidas) {
            e.preventDefault();
            mostrarAlerta('Debe ingresar el número de serie para los activos que lo requieren', 'warning');
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

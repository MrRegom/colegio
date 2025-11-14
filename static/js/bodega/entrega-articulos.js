/**
 * JavaScript para gestión de entregas de artículos
 * Siguiendo buenas prácticas de JavaScript moderno y Django
 */

// Configuración global
const EntregaArticulos = {
    articulosDisponibles: [],
    detallesArticulos: [],
    contadorFilas: 0,
    esSolicitud: false,

    /**
     * Inicializa el módulo
     */
    init(articulos) {
        this.articulosDisponibles = articulos;
        this.setupEventListeners();
        console.log('EntregaArticulos inicializado correctamente');
    },

    /**
     * Configura event listeners
     */
    setupEventListeners() {
        // Event listener para el selector de solicitud
        const selectSolicitud = document.getElementById('id_solicitud');
        if (selectSolicitud) {
            selectSolicitud.addEventListener('change', (e) => {
                const solicitudId = e.target.value;
                if (solicitudId) {
                    this.cargarArticulosSolicitud(solicitudId);
                } else {
                    this.limpiarArticulosSolicitud();
                }
            });
        }

        // Event listener para el botón de agregar artículo
        const btnAgregar = document.getElementById('btnAgregarArticulo');
        if (btnAgregar) {
            btnAgregar.addEventListener('click', () => this.agregarArticulo());
        }

        // Event listener para el submit del formulario
        const form = document.getElementById('formEntregaArticulo');
        if (form) {
            form.addEventListener('submit', (e) => this.validarYEnviarFormulario(e));
        }
    },

    /**
     * Carga artículos de una solicitud via AJAX
     */
    async cargarArticulosSolicitud(solicitudId) {
        try {
            const response = await fetch(`/bodega/ajax/solicitud/${solicitudId}/articulos/`);
            const data = await response.json();

            if (data.success) {
                this.esSolicitud = true;
                this.mostrarInfoSolicitud(data.solicitud);
                this.mostrarColumnasSolicitud();
                this.cargarArticulosEnTabla(data.articulos);

                // Deshabilitar botón de agregar artículo manual
                const btnAgregar = document.getElementById('btnAgregarArticulo');
                if (btnAgregar) {
                    btnAgregar.disabled = true;
                }

                // Auto-seleccionar bodega origen si está disponible
                if (data.solicitud.bodega_origen_id) {
                    const selectBodega = document.getElementById('id_bodega_origen');
                    if (selectBodega) {
                        selectBodega.value = data.solicitud.bodega_origen_id;
                    }
                }
            } else {
                alert('Error al cargar artículos de la solicitud: ' + (data.error || data.message));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al cargar artículos de la solicitud.');
        }
    },

    /**
     * Limpia datos de solicitud
     */
    limpiarArticulosSolicitud() {
        this.esSolicitud = false;
        const infoDiv = document.getElementById('infoSolicitud');
        if (infoDiv) {
            infoDiv.classList.add('d-none');
        }
        this.ocultarColumnasSolicitud();
        this.limpiarTabla();

        const btnAgregar = document.getElementById('btnAgregarArticulo');
        if (btnAgregar) {
            btnAgregar.disabled = false;
        }
    },

    /**
     * Muestra información de la solicitud
     */
    mostrarInfoSolicitud(solicitud) {
        const infoDiv = document.getElementById('infoSolicitud');
        const datosDiv = document.getElementById('datosSolicitud');

        if (!infoDiv || !datosDiv) return;

        datosDiv.innerHTML = `
            <p class="mb-1"><strong>Número:</strong> ${solicitud.numero}</p>
            <p class="mb-1"><strong>Solicitante:</strong> ${solicitud.solicitante}</p>
            <p class="mb-1"><strong>Departamento:</strong> ${solicitud.departamento}</p>
            <p class="mb-0"><strong>Motivo:</strong> ${solicitud.motivo || 'N/A'}</p>
        `;

        infoDiv.classList.remove('d-none');
    },

    /**
     * Muestra columnas adicionales para solicitud (sin columnas extra)
     */
    mostrarColumnasSolicitud() {
        // Ya no hay columnas adicionales, solo mantener para compatibilidad
    },

    /**
     * Oculta columnas adicionales de solicitud (sin columnas extra)
     */
    ocultarColumnasSolicitud() {
        // Ya no hay columnas adicionales, solo mantener para compatibilidad
    },

    /**
     * Carga artículos en la tabla
     */
    cargarArticulosEnTabla(articulos) {
        const tbody = document.getElementById('articulosBody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (articulos.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted">
                        No hay artículos en esta solicitud.
                    </td>
                </tr>
            `;
            return;
        }

        articulos.forEach(art => this.agregarFilaSolicitud(art));
    },

    /**
     * Agrega una fila desde solicitud
     */
    agregarFilaSolicitud(articulo) {
        const tbody = document.getElementById('articulosBody');
        if (!tbody) return;

        const fila = tbody.insertRow();
        fila.id = `fila_${this.contadorFilas}`;

        // Celda de artículo (solo lectura)
        const celdaArticulo = fila.insertCell(0);
        celdaArticulo.innerHTML = `
            <strong>${this.escapeHtml(articulo.articulo_codigo)}</strong><br>
            <small>${this.escapeHtml(articulo.articulo_nombre)}</small><br>
            <small class="text-muted">Pendiente: ${articulo.cantidad_pendiente} ${this.escapeHtml(articulo.unidad_medida)}</small>
            <input type="hidden" id="articulo_${this.contadorFilas}" value="${articulo.articulo_id}">
            <input type="hidden" id="detalle_solicitud_${this.contadorFilas}" value="${articulo.detalle_solicitud_id}">
        `;

        // Celda de stock disponible
        const celdaStock = fila.insertCell(1);
        const colorStock = articulo.stock_actual > 0 ? 'text-success' : 'text-danger';
        celdaStock.innerHTML = `<strong class="${colorStock}">${articulo.stock_actual} ${this.escapeHtml(articulo.unidad_medida)}</strong>`;

        // Celda de cantidad a entregar
        const celdaCantidad = fila.insertCell(2);
        const inputCantidad = this.crearInputCantidad(this.contadorFilas, articulo);
        celdaCantidad.appendChild(inputCantidad);

        // Celda de lote
        const celdaLote = fila.insertCell(3);
        const inputLote = this.crearInputLote(this.contadorFilas);
        celdaLote.appendChild(inputLote);

        // Celda de acciones (sin botón eliminar para solicitud)
        fila.insertCell(4).innerHTML = '<span class="text-muted">-</span>';

        this.contadorFilas++;
    },

    /**
     * Agrega una fila manual
     */
    agregarArticulo() {
        const tbody = document.getElementById('articulosBody');
        if (!tbody) return;

        // Limpiar fila vacía si existe
        if (tbody.children.length === 1 && tbody.children[0].cells.length === 1) {
            tbody.innerHTML = '';
        }

        const fila = tbody.insertRow();
        fila.id = `fila_${this.contadorFilas}`;
        const idFila = this.contadorFilas;

        // Celda de selección de artículo
        const celdaArticulo = fila.insertCell(0);
        const selectArticulo = this.crearSelectArticulo(idFila);
        celdaArticulo.appendChild(selectArticulo);

        // Celda de stock disponible
        const celdaStock = fila.insertCell(1);
        celdaStock.innerHTML = `<span id="stock_${idFila}" class="text-muted">-</span>`;

        // Celda de cantidad
        const celdaCantidad = fila.insertCell(2);
        const inputCantidad = this.crearInputCantidad(idFila);
        celdaCantidad.appendChild(inputCantidad);

        // Celda de lote
        const celdaLote = fila.insertCell(3);
        const inputLote = this.crearInputLote(idFila);
        celdaLote.appendChild(inputLote);

        // Celda de acciones
        const celdaAcciones = fila.insertCell(4);
        const btnEliminar = this.crearBotonEliminar(idFila);
        celdaAcciones.appendChild(btnEliminar);

        this.contadorFilas++;
    },

    /**
     * Crea select de artículos
     */
    crearSelectArticulo(idFila) {
        const select = document.createElement('select');
        select.className = 'form-select form-select-sm';
        select.id = `articulo_${idFila}`;
        select.innerHTML = '<option value="">Seleccione...</option>';

        this.articulosDisponibles.forEach(art => {
            select.innerHTML += `<option value="${art.id}" data-stock="${art.stock}" data-unidad="${this.escapeHtml(art.unidad)}">
                ${this.escapeHtml(art.codigo)} - ${this.escapeHtml(art.nombre)}
            </option>`;
        });

        select.addEventListener('change', () => this.actualizarStock(idFila));

        return select;
    },

    /**
     * Crea input de cantidad
     */
    crearInputCantidad(idFila, articulo = null) {
        const input = document.createElement('input');
        input.type = 'number';
        input.className = 'form-control form-control-sm';
        input.id = `cantidad_${idFila}`;
        input.step = '0.01';
        input.min = '0.01';
        input.required = true;

        if (articulo) {
            input.max = articulo.cantidad_pendiente;
            input.value = articulo.cantidad_pendiente;
            input.setAttribute('data-pendiente', articulo.cantidad_pendiente);
            input.setAttribute('data-stock', articulo.stock_actual);
        }

        return input;
    },

    /**
     * Crea input de lote
     */
    crearInputLote(idFila) {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'form-control form-control-sm';
        input.id = `lote_${idFila}`;
        input.placeholder = 'Lote (opcional)';
        return input;
    },

    /**
     * Crea botón de eliminar
     */
    crearBotonEliminar(idFila) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-sm btn-danger';
        btn.innerHTML = '<i class="ri-delete-bin-line"></i>';
        btn.addEventListener('click', () => this.eliminarFila(idFila));
        return btn;
    },

    /**
     * Actualiza el stock mostrado
     */
    actualizarStock(idFila) {
        const select = document.getElementById(`articulo_${idFila}`);
        const spanStock = document.getElementById(`stock_${idFila}`);

        if (!select || !spanStock) return;

        if (select.value) {
            const opcion = select.options[select.selectedIndex];
            const stock = opcion.getAttribute('data-stock');
            const unidad = opcion.getAttribute('data-unidad');
            spanStock.innerHTML = `<strong>${stock} ${unidad}</strong>`;
            spanStock.className = parseFloat(stock) > 0 ? 'text-success' : 'text-danger';
        } else {
            spanStock.innerHTML = '<span class="text-muted">-</span>';
        }
    },

    /**
     * Elimina una fila de la tabla
     */
    eliminarFila(idFila) {
        const fila = document.getElementById(`fila_${idFila}`);
        if (fila) {
            fila.remove();
        }

        // Si no quedan filas, mostrar mensaje
        const tbody = document.getElementById('articulosBody');
        if (tbody && tbody.children.length === 0) {
            this.limpiarTabla();
        }
    },

    /**
     * Limpia la tabla
     */
    limpiarTabla() {
        const tbody = document.getElementById('articulosBody');
        if (!tbody) return;

        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-muted">
                    No hay artículos agregados. Seleccione una solicitud o haga clic en "Agregar Artículo" para comenzar.
                </td>
            </tr>
        `;
        this.contadorFilas = 0;
    },

    /**
     * Valida y envía el formulario
     */
    validarYEnviarFormulario(e) {
        e.preventDefault();

        const detalles = [];
        const tbody = document.getElementById('articulosBody');

        // Validar que haya artículos
        if (!tbody || tbody.children.length === 0 || tbody.children[0].cells.length === 1) {
            alert('Debe agregar al menos un artículo a la entrega.');
            return false;
        }

        // Recorrer filas y construir array de detalles
        for (let i = 0; i < this.contadorFilas; i++) {
            const fila = document.getElementById(`fila_${i}`);
            if (!fila) continue;

            const inputCantidad = document.getElementById(`cantidad_${i}`);
            const inputLote = document.getElementById(`lote_${i}`);

            if (!inputCantidad) continue;

            let articuloId, detalleSolicitudId = null;

            if (this.esSolicitud) {
                // Modo solicitud
                const inputArticulo = document.getElementById(`articulo_${i}`);
                const inputDetalleSolicitud = document.getElementById(`detalle_solicitud_${i}`);

                if (!inputArticulo || !inputDetalleSolicitud) continue;

                articuloId = parseInt(inputArticulo.value);
                detalleSolicitudId = parseInt(inputDetalleSolicitud.value);

                // Validaciones
                if (!this.validarCantidadSolicitud(inputCantidad)) {
                    return false;
                }
            } else {
                // Modo manual
                const selectArticulo = document.getElementById(`articulo_${i}`);

                if (!selectArticulo || !selectArticulo.value) {
                    alert('Seleccione un artículo en todas las filas.');
                    return false;
                }

                articuloId = parseInt(selectArticulo.value);

                // Validar stock disponible
                if (!this.validarStockDisponible(selectArticulo, inputCantidad)) {
                    return false;
                }
            }

            if (!inputCantidad.value || parseFloat(inputCantidad.value) <= 0) {
                alert('Ingrese una cantidad válida en todas las filas.');
                return false;
            }

            const detalle = {
                articulo_id: articuloId,
                cantidad: parseFloat(inputCantidad.value),
                lote: inputLote ? (inputLote.value || null) : null
            };

            if (detalleSolicitudId) {
                detalle.detalle_solicitud_id = detalleSolicitudId;
            }

            detalles.push(detalle);
        }

        // Guardar JSON en campo oculto
        const detallesInput = document.getElementById('detallesJson');
        if (detallesInput) {
            detallesInput.value = JSON.stringify(detalles);
        }

        // Enviar formulario
        e.target.submit();
        return true;
    },

    /**
     * Valida cantidad en modo solicitud
     */
    validarCantidadSolicitud(inputCantidad) {
        const cantidadPendiente = parseFloat(inputCantidad.getAttribute('data-pendiente'));
        const cantidadAEntregar = parseFloat(inputCantidad.value);
        const stockDisponible = parseFloat(inputCantidad.getAttribute('data-stock'));

        if (cantidadAEntregar > cantidadPendiente) {
            alert(`La cantidad a entregar (${cantidadAEntregar}) excede la cantidad pendiente (${cantidadPendiente}).`);
            return false;
        }

        if (cantidadAEntregar > stockDisponible) {
            alert(`La cantidad a entregar (${cantidadAEntregar}) excede el stock disponible (${stockDisponible}).`);
            return false;
        }

        return true;
    },

    /**
     * Valida stock disponible en modo manual
     */
    validarStockDisponible(selectArticulo, inputCantidad) {
        const opcion = selectArticulo.options[selectArticulo.selectedIndex];
        const stockDisponible = parseFloat(opcion.getAttribute('data-stock'));
        const cantidadSolicitada = parseFloat(inputCantidad.value);

        if (cantidadSolicitada > stockDisponible) {
            alert(`La cantidad solicitada (${cantidadSolicitada}) excede el stock disponible (${stockDisponible}).`);
            return false;
        }

        return true;
    },

    /**
     * Escapa HTML para prevenir XSS
     */
    escapeHtml(unsafe) {
        if (!unsafe) return '';
        return unsafe
            .toString()
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
};

// Exportar para uso global
window.EntregaArticulos = EntregaArticulos;

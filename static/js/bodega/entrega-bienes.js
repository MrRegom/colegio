/**
 * JavaScript para gestión de entregas de bienes/activos
 * Siguiendo buenas prácticas de JavaScript moderno y Django
 */

const EntregaBienes = {
    activosDisponibles: [],
    detallesBienes: [],
    contadorFilas: 0,

    /**
     * Inicializa el módulo
     */
    init(activos) {
        this.activosDisponibles = activos;
        this.setupEventListeners();
        console.log('EntregaBienes inicializado correctamente');
    },

    /**
     * Configura event listeners
     */
    setupEventListeners() {
        // Event listener para el botón de agregar bien
        const btnAgregar = document.getElementById('btnAgregarBien');
        if (btnAgregar) {
            btnAgregar.addEventListener('click', () => this.agregarBien());
        }

        // Event listener para el submit del formulario
        const form = document.getElementById('formEntregaBien');
        if (form) {
            form.addEventListener('submit', (e) => this.validarYEnviarFormulario(e));
        }
    },

    /**
     * Agrega una fila de bien
     */
    agregarBien() {
        const tbody = document.getElementById('bienesBody');
        if (!tbody) return;

        // Limpiar fila vacía si existe
        if (tbody.children.length === 1 && tbody.children[0].cells.length === 1) {
            tbody.innerHTML = '';
        }

        const fila = tbody.insertRow();
        fila.id = `fila_${this.contadorFilas}`;
        const idFila = this.contadorFilas;

        // Celda de selección de activo
        const celdaActivo = fila.insertCell(0);
        const selectActivo = this.crearSelectActivo(idFila);
        celdaActivo.appendChild(selectActivo);

        // Celda de cantidad
        const celdaCantidad = fila.insertCell(1);
        const inputCantidad = this.crearInputCantidad(idFila);
        celdaCantidad.appendChild(inputCantidad);

        // Celda de número de serie
        const celdaSerie = fila.insertCell(2);
        const inputSerie = this.crearInputSerie(idFila);
        celdaSerie.appendChild(inputSerie);

        // Celda de estado físico
        const celdaEstado = fila.insertCell(3);
        const selectEstado = this.crearSelectEstado(idFila);
        celdaEstado.appendChild(selectEstado);

        // Celda de acciones
        const celdaAcciones = fila.insertCell(4);
        const btnEliminar = this.crearBotonEliminar(idFila);
        celdaAcciones.appendChild(btnEliminar);

        this.contadorFilas++;
    },

    /**
     * Crea select de activos
     */
    crearSelectActivo(idFila) {
        const select = document.createElement('select');
        select.className = 'form-select form-select-sm';
        select.id = `activo_${idFila}`;
        select.required = true;
        select.innerHTML = '<option value="">Seleccione...</option>';

        this.activosDisponibles.forEach(activo => {
            const categoria = activo.categoria || '-';
            const codigo = activo.codigo || '';
            select.innerHTML += `<option value="${activo.id}">
                ${this.escapeHtml(activo.nombre)} - ${this.escapeHtml(codigo)} (${this.escapeHtml(categoria)})
            </option>`;
        });

        return select;
    },

    /**
     * Crea input de cantidad
     */
    crearInputCantidad(idFila) {
        const input = document.createElement('input');
        input.type = 'number';
        input.className = 'form-control form-control-sm';
        input.id = `cantidad_${idFila}`;
        input.step = '1';
        input.min = '1';
        input.value = '1';
        input.required = true;
        return input;
    },

    /**
     * Crea input de número de serie
     */
    crearInputSerie(idFila) {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'form-control form-control-sm';
        input.id = `serie_${idFila}`;
        input.placeholder = 'Número de serie (opcional)';
        return input;
    },

    /**
     * Crea select de estado físico
     */
    crearSelectEstado(idFila) {
        const select = document.createElement('select');
        select.className = 'form-select form-select-sm';
        select.id = `estado_fisico_${idFila}`;
        select.innerHTML = `
            <option value="">Seleccione...</option>
            <option value="EXCELENTE">Excelente</option>
            <option value="BUENO">Bueno</option>
            <option value="REGULAR">Regular</option>
            <option value="MALO">Malo</option>
        `;
        return select;
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
     * Elimina una fila de la tabla
     */
    eliminarFila(idFila) {
        const fila = document.getElementById(`fila_${idFila}`);
        if (fila) {
            fila.remove();
        }

        // Si no quedan filas, mostrar mensaje
        const tbody = document.getElementById('bienesBody');
        if (tbody && tbody.children.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted">
                        No hay bienes agregados. Haga clic en "Agregar Bien" para comenzar.
                    </td>
                </tr>
            `;
        }
    },

    /**
     * Valida y envía el formulario
     */
    validarYEnviarFormulario(e) {
        e.preventDefault();

        const detalles = [];
        const tbody = document.getElementById('bienesBody');

        // Validar que haya bienes
        if (!tbody || tbody.children.length === 0 || tbody.children[0].cells.length === 1) {
            alert('Debe agregar al menos un bien a la entrega.');
            return false;
        }

        // Recorrer filas y construir array de detalles
        for (let i = 0; i < this.contadorFilas; i++) {
            const fila = document.getElementById(`fila_${i}`);
            if (!fila) continue;

            const selectActivo = document.getElementById(`activo_${i}`);
            const inputCantidad = document.getElementById(`cantidad_${i}`);
            const inputSerie = document.getElementById(`serie_${i}`);
            const selectEstado = document.getElementById(`estado_fisico_${i}`);

            if (!selectActivo || !selectActivo.value) {
                alert('Seleccione un activo/bien en todas las filas.');
                return false;
            }

            if (!inputCantidad || !inputCantidad.value || parseInt(inputCantidad.value) <= 0) {
                alert('Ingrese una cantidad válida en todas las filas.');
                return false;
            }

            detalles.push({
                equipo_id: parseInt(selectActivo.value),
                cantidad: parseInt(inputCantidad.value),
                numero_serie: inputSerie ? (inputSerie.value || null) : null,
                estado_fisico: selectEstado ? (selectEstado.value || null) : null
            });
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
window.EntregaBienes = EntregaBienes;

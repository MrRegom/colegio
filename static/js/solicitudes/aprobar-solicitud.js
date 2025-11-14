/**
 * Validaciones para el formulario de aprobación de solicitudes
 * @module solicitudes/aprobar-solicitud
 * @description Valida las cantidades aprobadas antes de enviar el formulario
 */

(function() {
    'use strict';

    /**
     * Inicializa las validaciones del formulario
     */
    function inicializarValidaciones() {
        const cantidadInputs = document.querySelectorAll('.cantidad-input');
        const form = document.querySelector('form');

        if (!form || cantidadInputs.length === 0) {
            return;
        }

        // Agregar validación en tiempo real a cada input
        cantidadInputs.forEach(input => {
            input.addEventListener('input', function() {
                validarCantidad(this);
            });
        });

        // Validar antes de enviar el formulario
        form.addEventListener('submit', function(e) {
            if (!validarFormulario(cantidadInputs)) {
                e.preventDefault();
                mostrarAlertaError();
                return false;
            }
        });
    }

    /**
     * Valida un campo de cantidad individual
     * @param {HTMLInputElement} input - Campo de cantidad a validar
     */
    function validarCantidad(input) {
        const valorActual = parseFloat(input.value) || 0;
        const maxPermitido = parseFloat(input.getAttribute('data-max'));
        const parentTd = input.closest('td');

        // Remover mensajes de error anteriores
        limpiarErrores(parentTd);

        // Validar que no exceda el máximo
        if (valorActual > maxPermitido) {
            marcarComoInvalido(input);
            mostrarError(parentTd, `La cantidad no puede exceder ${maxPermitido}`);
            return false;
        }

        // Validar que no sea negativo
        if (valorActual < 0) {
            marcarComoInvalido(input);
            mostrarError(parentTd, 'La cantidad no puede ser negativa');
            return false;
        }

        // Si es válido, remover clase de error
        input.classList.remove('is-invalid');
        return true;
    }

    /**
     * Valida todos los campos del formulario
     * @param {NodeList} cantidadInputs - Lista de inputs de cantidad
     * @returns {boolean} - True si todos los campos son válidos
     */
    function validarFormulario(cantidadInputs) {
        let hayErrores = false;

        cantidadInputs.forEach(input => {
            const valorActual = parseFloat(input.value);
            const maxPermitido = parseFloat(input.getAttribute('data-max'));
            const parentTd = input.closest('td');

            // Validar que no esté vacío
            if (isNaN(valorActual) || input.value === '' || input.value === null) {
                hayErrores = true;
                marcarComoInvalido(input);
                mostrarError(parentTd, 'Este campo es obligatorio');
                return;
            }

            // Validar que no exceda el máximo
            if (valorActual > maxPermitido) {
                hayErrores = true;
                marcarComoInvalido(input);
                mostrarError(parentTd, `La cantidad no puede exceder ${maxPermitido}`);
                return;
            }

            // Validar que no sea negativo
            if (valorActual < 0) {
                hayErrores = true;
                marcarComoInvalido(input);
                mostrarError(parentTd, 'La cantidad no puede ser negativa');
                return;
            }
        });

        return !hayErrores;
    }

    /**
     * Limpia los mensajes de error de un contenedor
     * @param {HTMLElement} contenedor - Elemento contenedor
     */
    function limpiarErrores(contenedor) {
        const errorAnterior = contenedor.querySelector('.validation-error');
        if (errorAnterior) {
            errorAnterior.remove();
        }
    }

    /**
     * Marca un input como inválido
     * @param {HTMLInputElement} input - Campo a marcar
     */
    function marcarComoInvalido(input) {
        input.classList.add('is-invalid');
    }

    /**
     * Muestra un mensaje de error debajo de un campo
     * @param {HTMLElement} contenedor - Contenedor donde mostrar el error
     * @param {string} mensaje - Mensaje de error a mostrar
     */
    function mostrarError(contenedor, mensaje) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'text-danger small mt-1 validation-error';
        errorDiv.textContent = mensaje;
        contenedor.appendChild(errorDiv);
    }

    /**
     * Muestra una alerta cuando hay errores en el formulario
     */
    function mostrarAlertaError() {
        alert('Por favor corrija los errores en el formulario antes de continuar.');
    }

    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', inicializarValidaciones);
    } else {
        inicializarValidaciones();
    }

})();

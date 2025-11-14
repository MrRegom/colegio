/**
 * Correo Masivo - Enviar Correo
 * Funciones JavaScript para el editor de correos masivos
 */

// Variables globales
let listaSeleccionada = null;

document.addEventListener('DOMContentLoaded', function() {
    // Configurar contenido editable
    const contenidoDiv = document.getElementById('contenido');
    const contenidoHidden = document.getElementById('contenido-hidden');
    
    contenidoDiv.addEventListener('input', function() {
        contenidoHidden.value = this.innerHTML;
    });

    // Programación de envío
    const programarCheckbox = document.getElementById('programar-envio');
    const programacionFields = document.getElementById('programacion-fields');
    
    programarCheckbox.addEventListener('change', function() {
        programacionFields.style.display = this.checked ? 'block' : 'none';
    });

    // Envío del formulario
    document.getElementById('correoForm').addEventListener('submit', function(e) {
        e.preventDefault();
        enviarCorreo();
    });
});

// Funciones del editor de texto
function formatText(command) {
    document.execCommand(command, false, null);
    document.getElementById('contenido').focus();
    // Actualizar campo hidden
    document.getElementById('contenido-hidden').value = document.getElementById('contenido').innerHTML;
}

function insertVariable(variable) {
    const contenido = document.getElementById('contenido');
    const variableText = `{${variable}}`;
    
    // Usar execCommand para mejor compatibilidad
    document.execCommand('insertText', false, variableText);
    contenido.focus();
    
    // Actualizar campo hidden
    document.getElementById('contenido-hidden').value = contenido.innerHTML;
}

function insertSignature() {
    // Obtener firma del usuario mediante AJAX
    fetch('/correo_masivo/firma/?action=get_user_signature', {
        method: 'GET',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.html_firma) {
            const contenido = document.getElementById('contenido');
            
            // Insertar firma al final del contenido
            const currentContent = contenido.innerHTML;
            const signatureHTML = `
                <br><br>
                <div class="email-signature">
                    ${data.html_firma}
                </div>
            `;
            
            contenido.innerHTML = currentContent + signatureHTML;
            document.getElementById('contenido-hidden').value = contenido.innerHTML;
            
            Toastify({
                text: "✅ Firma insertada correctamente",
                duration: 2000,
                gravity: "top",
                position: "right",
                backgroundColor: "#28a745"
            }).showToast();
        } else {
            Toastify({
                text: "❌ No se encontró firma configurada. Vaya a Gestionar Firma para crear una.",
                duration: 4000,
                gravity: "top",
                position: "right",
                backgroundColor: "#dc3545"
            }).showToast();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Toastify({
            text: "❌ Error al cargar la firma",
            duration: 3000,
            gravity: "top",
            position: "right",
            backgroundColor: "#dc3545"
        }).showToast();
    });
}

function insertImage() {
    // Crear input file temporal
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (file) {
            // Validar tamaño (máximo 2MB)
            if (file.size > 2 * 1024 * 1024) {
                Toastify({
                    text: "❌ La imagen debe ser menor a 2MB",
                    duration: 3000,
                    gravity: "top",
                    position: "right",
                    backgroundColor: "#dc3545"
                }).showToast();
                return;
            }
            
            // Convertir a base64 para insertar
            const reader = new FileReader();
            reader.onload = function(e) {
                const imageHTML = `<img src="${e.target.result}" style="max-width: 100%; height: auto; margin: 10px 0;" alt="Imagen insertada">`;
                
                // Insertar en el contenido
                const contenido = document.getElementById('contenido');
                document.execCommand('insertHTML', false, imageHTML);
                document.getElementById('contenido-hidden').value = contenido.innerHTML;
                
                Toastify({
                    text: "✅ Imagen insertada correctamente",
                    duration: 2000,
                    gravity: "top",
                    position: "right",
                    backgroundColor: "#28a745"
                }).showToast();
            };
            reader.readAsDataURL(file);
        }
    };
    
    input.click();
}

// Funciones del modal de listas de remitentes
function seleccionarLista(id, nombre, totalFuncionarios) {
    // Marcar radio button
    document.getElementById('lista_' + id).checked = true;
    
    // Habilitar botón de confirmación
    document.getElementById('btnConfirmarSeleccion').disabled = false;
    
    // Guardar datos de la lista seleccionada temporalmente
    window.listaSeleccionadaTemp = {
        id: id,
        nombre: nombre,
        totalFuncionarios: totalFuncionarios
    };
}

function confirmarSeleccion() {
    if (window.listaSeleccionadaTemp) {
        listaSeleccionada = window.listaSeleccionadaTemp;
        
        // Actualizar display
        mostrarListaSeleccionada(listaSeleccionada);
        
        // Cerrar modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('seleccionarListaModal'));
        modal.hide();
        
        // Notificación
        Toastify({
            text: `Lista "${listaSeleccionada.nombre}" seleccionada correctamente`,
            duration: 3000,
            gravity: "top",
            position: "right",
            backgroundColor: "#28a745"
        }).showToast();
    }
}

function mostrarListaSeleccionada(lista) {
    const container = document.getElementById('lista-seleccionada');
    const contador = document.getElementById('contador-destinatarios');
    
    if (!lista) {
        container.innerHTML = '<p class="text-muted mb-0"><i class="ri-information-line"></i> No hay lista seleccionada</p>';
        contador.textContent = '0';
        return;
    }
    
    const html = `
        <div class="d-flex align-items-center">
            <div class="flex-shrink-0 me-2">
                <div class="avatar-xs">
                    <div class="avatar-title bg-success-subtle text-success rounded-circle fs-13">
                        <i class="ri-mail-send-line"></i>
                    </div>
                </div>
            </div>
            <div class="flex-grow-1">
                <h6 class="fs-14 mb-0">${lista.nombre}</h6>
                <small class="text-muted">${lista.totalFuncionarios} funcionarios</small>
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger" onclick="limpiarSeleccion()">
                <i class="ri-close-line"></i>
            </button>
        </div>
    `;
    
    container.innerHTML = html;
    contador.textContent = lista.totalFuncionarios;
}

function limpiarSeleccion() {
    listaSeleccionada = null;
    mostrarListaSeleccionada(null);
    
    Toastify({
        text: "Selección de lista limpiada",
        duration: 2000,
        gravity: "top",
        position: "right",
        backgroundColor: "#6c757d"
    }).showToast();
}

function removerDestinatario(id) {
    // Implementar lógica para remover destinatario específico
    console.log('Remover destinatario:', id);
}

function previsualizarCorreo() {
    const asunto = document.getElementById('asunto').value.trim();
    const contenido = document.getElementById('contenido').innerHTML.trim();
    
    if (!asunto || !contenido || contenido === '<br>' || contenido === '<div><br></div>') {
        Toastify({
            text: "Complete el asunto y contenido antes de previsualizar",
            duration: 3000,
            gravity: "top",
            position: "right",
            backgroundColor: "#dc3545"
        }).showToast();
        return;
    }

    // Ejemplo de contenido con variables reemplazadas
    const contenidoEjemplo = contenido
        .replace(/{nombre}/g, 'Juan Pérez López')
        .replace(/{email}/g, 'juan.perez@hospital.com')
        .replace(/{unidad}/g, 'Informática');

    const previewContent = `
        <div class="email-preview">
            <div class="border rounded p-3 bg-light mb-3">
                <h6 class="mb-1"><i class="ri-mail-line text-primary"></i> <strong>Asunto:</strong></h6>
                <p class="mb-0">${asunto}</p>
            </div>
            
            <div class="border rounded p-3">
                <h6 class="mb-3"><i class="ri-file-text-line text-info"></i> <strong>Contenido del Correo:</strong></h6>
                <div class="email-content" style="line-height: 1.6;">${contenidoEjemplo}</div>
            </div>
            
            <div class="alert alert-info mt-3 mb-0">
                <i class="ri-information-line me-1"></i>
                <strong>Vista previa con datos de ejemplo:</strong> Las variables {nombre}, {email}, {unidad} se reemplazarán automáticamente con los datos reales de cada destinatario.
            </div>
        </div>
    `;
    
    document.getElementById('preview-content').innerHTML = previewContent;
    new bootstrap.Modal(document.getElementById('previewModal')).show();
}

function guardarBorrador() {
    Toastify({
        text: "La función de guardar borrador estará disponible próximamente",
        duration: 3000,
        gravity: "top",
        position: "right",
        backgroundColor: "#17a2b8"
    }).showToast();
}

function enviarCorreo() {
    const formData = new FormData(document.getElementById('correoForm'));
    
    // Actualizar contenido oculto
    document.getElementById('contenido-hidden').value = document.getElementById('contenido').innerHTML;
    
    // Validar que se haya seleccionado una lista
    if (!listaSeleccionada) {
        Toastify({
            text: "❌ Debe seleccionar una lista de remitentes",
            duration: 3000,
            gravity: "top",
            position: "right",
            backgroundColor: "#dc3545"
        }).showToast();
        return;
    }
    
    // Agregar ID de lista seleccionada
    formData.append('lista_remitentes_id', listaSeleccionada.id);
    
    fetch(window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            Toastify({
                text: `✅ ${data.message || 'Correo enviado exitosamente'}`,
                duration: 4000,
                gravity: "top",
                position: "right",
                backgroundColor: "#28a745"
            }).showToast();
            
            // Limpiar formulario después de un momento
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        } else {
            let errorMsg = 'Errores encontrados: ';
            if (data.errors && data.errors.length > 0) {
                errorMsg += data.errors.join(', ');
            } else {
                errorMsg += data.message || 'Error desconocido';
            }
            
            Toastify({
                text: `❌ ${errorMsg}`,
                duration: 5000,
                gravity: "top",
                position: "right",
                backgroundColor: "#dc3545"
            }).showToast();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Toastify({
            text: "❌ Ocurrió un error al enviar el correo",
            duration: 4000,
            gravity: "top",
            position: "right",
            backgroundColor: "#dc3545"
        }).showToast();
    });
}

/*
* Formulario de solicitud de perfiles - Inicialización
*/

// Función para enviar el formulario por correo
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si SweetAlert está disponible
    if (typeof Swal === 'undefined') {
        console.error('SweetAlert2 no está disponible. Asegúrese de incluir la biblioteca correctamente.');
        return;
    }
    
    // Obtener referencia al formulario y botones
    const profileForm = document.getElementById('profileRequestForm');
    const submitButton = document.getElementById('submitToLeadership');
    const signatureButton = document.getElementById('leadershipSignature');
    
    // Cargar datos desde URL si estamos en modo solo lectura
    loadReadOnlyForm();
    
    if (profileForm && submitButton) {
        submitButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Validar el formulario
            if (!profileForm.checkValidity()) {
                profileForm.classList.add('was-validated');
                return;
            }
            
            // Recoger datos del formulario
            const userData = {
                firstName: document.getElementById('firstnamefloatingInput').value,
                lastName: document.getElementById('lastnamefloatingInput').value,
                rut: document.getElementById('rutfloatingInput').value,
                email: document.getElementById('emailfloatingInput').value,
                unit: document.getElementById('unidadfloatingInput1').value,
                estamento: document.getElementById('estamentofloatingInput').value,
                position: document.getElementById('cargofloatingInput').value
            };
            
            const leadershipEmail = document.getElementById('emailleadershipfloatingInput').value;
            
            if (!leadershipEmail) {
                // Mostrar alerta si no se ha ingresado el correo de la jefatura
                Swal.fire({
                    title: 'Error',
                    text: 'Debe ingresar el correo electrónico de la jefatura',
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary w-xs mt-2'
                    },
                    buttonsStyling: false
                });
                return;
            }
            
            // Crear URL con los datos del formulario para el modo de solo lectura
            let urlParams = new URLSearchParams();
            
            // Recoger todos los datos del formulario
            const inputs = profileForm.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                // Para checkboxes, solo añadir los seleccionados
                if ((input.type === 'checkbox' || input.type === 'radio') && !input.checked) {
                    return;
                }
                
                if (input.name && input.value) {
                    // Para campos con nombre, usar el nombre como parámetro
                    if (input.name.endsWith('[]')) {
                        // Para arrays (como sistema[]), añadir múltiples valores con el mismo nombre
                        if (input.checked) {
                            urlParams.append(input.name.slice(0, -2), input.value);
                        }
                    } else {
                        urlParams.append(input.name, input.value);
                    }
                } else if (input.id && input.value) {
                    // Para campos sin nombre pero con ID, usar el ID
                    urlParams.append(input.id, input.value);
                }
            });
            
            // Añadir el parámetro readonly
            urlParams.append('readonly', 'true');
            
                // Crear la URL completa
                const readOnlyUrl = window.location.origin + window.location.pathname + '?' + urlParams.toString();

                // Enviar el formulario llamando a la función global definida en form-perfil.js
                try {
                    if (typeof window.submitProfileForm === 'function') {
                        window.submitProfileForm();
                    } else if (typeof profileForm.requestSubmit === 'function') {
                        profileForm.requestSubmit();
                    } else {
                        const evt = new Event('submit', { cancelable: true });
                        profileForm.dispatchEvent(evt);
                    }
                } catch (err) {
                    console.error('No se pudo enviar el formulario automáticamente:', err);
                }
        
            // Preparar el cuerpo del correo
            //const emailBody = `
                //Buenas tardes,

                //El presente correo es para solicitar su firma y poder gestionar la creación de perfiles para el funcionario/a:

                // if (profileForm && submitButton) {
                //     submitButton.addEventListener('click', function(e) {
                //         e.preventDefault();
                //         
                //         // Validar el formulario
                //         if (!profileForm.checkValidity()) {
                //             profileForm.classList.add('was-validated');
                //             return;
                //         }
                //         
                //         // Recoger datos del formulario
                //         const userData = {
                //             firstName: document.getElementById('firstnamefloatingInput').value,
                //             lastName: document.getElementById('lastnamefloatingInput').value,
                //             rut: document.getElementById('rutfloatingInput').value,
                //             email: document.getElementById('emailfloatingInput').value,
                //             unit: document.getElementById('unidadfloatingInput1').value,
                //             estamento: document.getElementById('estamentofloatingInput').value,
                //             position: document.getElementById('cargofloatingInput').value
                //         };
                //         
                //         const leadershipEmail = document.getElementById('emailleadershipfloatingInput').value;
                //         
                //         if (!leadershipEmail) {
                //             // Mostrar alerta si no se ha ingresado el correo de la jefatura
                //             Swal.fire({
                //                 title: 'Error',
                //                 text: 'Debe ingresar el correo electrónico de la jefatura',
                //                 icon: 'error',
                //                 customClass: {
                //                     confirmButton: 'btn btn-primary w-xs mt-2'
                //                 },
                //                 buttonsStyling: false
                //             });
                //             return;
                //         }
                //         
                //         // Crear URL con los datos del formulario para el modo de solo lectura
                //         let urlParams = new URLSearchParams();
                //         // Recoger todos los datos del formulario
                //         const inputs = profileForm.querySelectorAll('input, textarea, select');
                //         inputs.forEach(input => {
                //             // Para checkboxes, solo añadir los seleccionados
                //             if ((input.type === 'checkbox' || input.type === 'radio') && !input.checked) {
                //                 return;
                //             }
                //             
                //             if (input.name && input.value) {
                //                 // Para campos con nombre, usar el nombre como parámetro
                //                 if (input.name.endsWith('[]')) {
                //                     // Para arrays (como sistema[]), añadir múltiples valores con el mismo nombre
                //                     if (input.checked) {
                //                         urlParams.append(input.name.slice(0, -2), input.value);
                //                     }
                //                 } else {
                //                     urlParams.append(input.name, input.value);
                //                 }
                //             } else if (input.id && input.value) {
                //                 // Para campos sin nombre pero con ID, usar el ID
                //                 urlParams.append(input.id, input.value);
                //             }
                //         });
                //         
                //         // Añadir el parámetro readonly
                //         urlParams.append('readonly', 'true');
                //         
                //         // Crear la URL completa
                //         const readOnlyUrl = window.location.origin + window.location.pathname + '?' + urlParams.toString();
                //         
                //         // Preparar el cuerpo del correo
                //         const emailBody = `
                //             Buenas tardes,
                //
                //             El presente correo es para solicitar su firma y poder gestionar la creación de perfiles para el funcionario/a:
                //
                //             Nombres: ${userData.firstName} ${userData.lastName}
                //             RUT: ${userData.rut}
                //             Cargo: ${userData.position}
                //             
                //             Puede revisar y firmar el formulario completo en el siguiente enlace:
                //             ${readOnlyUrl}
                //
                //             Saludos cordiales,
                //         `;
                //         
                //         // Mostrar mensaje de carga con SweetAlert2
                //         let loadingAlert = Swal.fire({
                //             title: 'Enviando',
                //             text: 'Enviando formulario a la jefatura...',
                //             allowOutsideClick: false,
                //             allowEscapeKey: false,
                //             showConfirmButton: false,
                //             didOpen: () => {
                //                 Swal.showLoading();
                //             }
                //         });
                //         
                //         // Simular tiempo de espera para una solicitud real
                //         setTimeout(() => {
                //             // Cerrar el diálogo de carga
                //             loadingAlert.close();
                //             
                //             // Generar un pequeño retraso para evitar conflictos entre alertas
                //             setTimeout(() => {
                //                 // Mostrar mensaje de éxito con SweetAlert2
                //                 Swal.fire({
                //                     title: 'Enviado',
                //                     text: `El formulario ha sido enviado exitosamente a ${leadershipEmail}`,
                //                     icon: 'success',
                //                     customClass: {
                //                         confirmButton: 'btn btn-primary w-xs mt-2'
                //                     },
                //                     buttonsStyling: false
                //                 });
                //                 
                //                 // Logging (solo para desarrollo)
                //                 console.log('Datos del formulario:', userData);
                //                 console.log('Correo a enviar a:', leadershipEmail);
                //                 console.log('Cuerpo del correo:', emailBody);
                //                 console.log('URL de solo lectura:', readOnlyUrl);
                //             }, 200);
                //         }, 1500);
                //     });

/**
 * Session Timeout - Cierre automático de sesión por inactividad
 */

document.addEventListener('DOMContentLoaded', function() {
    // Tiempo de inactividad en milisegundos (1 minuto = 1 * 60 * 1000)
    const inactivityTime = 5 * 60 * 1000;
    let timeout;
    let warningShown = false;
    let logoutUrl = document.querySelector('a[href*="account_logout"]')?.getAttribute('href') || '/account/logout/';
    
    // Para sincronizar la actividad entre pestañas
    const LAST_ACTIVITY_TIME_KEY = 'lastActivityTime';
    const CHECK_INTERVAL = 10000; // Revisar cada 10 segundos
    
    // Obtener token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Actualizar el timestamp de última actividad
    function updateLastActivityTime() {
        localStorage.setItem(LAST_ACTIVITY_TIME_KEY, Date.now().toString());
    }
    
    // Obtener el timestamp de última actividad
    function getLastActivityTime() {
        const time = localStorage.getItem(LAST_ACTIVITY_TIME_KEY);
        return time ? parseInt(time, 10) : Date.now();
    }
    
    // Función para detectar actividad del usuario
    function handleUserActivity() {
        // Solo procesar eventos de actividad si no se está mostrando la advertencia
        if (!warningShown) {
            resetTimer();
        }
    }
    
    // Reiniciar el temporizador de inactividad
    function resetTimer() {
        clearTimeout(timeout);
        
        // Actualizar el timestamp de última actividad
        updateLastActivityTime();
        
        // Si se ha mostrado la advertencia, no la ocultamos aquí
        // Esto es para evitar que el movimiento del mouse cierre la advertencia
        
        // Configurar el nuevo temporizador
        timeout = setTimeout(function() {
            // Mostrar advertencia 30 segundos antes de cerrar sesión
            showWarning();
        }, inactivityTime - 30000); // Mostrar advertencia 30 segundos antes
    }
    
    // Mostrar la advertencia de cierre de sesión
    function showWarning() {
        if (!warningShown) { // Evitar mostrar múltiples advertencias
            warningShown = true;
            
            // Configuración de SweetAlert2
            const swalConfig = {
                title: 'Advertencia de cierre de sesión',
                text: 'Su sesión expirará en 30 segundos debido a inactividad.',
                icon: 'warning',
                timer: 30000,
                timerProgressBar: true,
                
                // Configuración de botones
                showCancelButton: true,
                showConfirmButton: true,
                confirmButtonText: 'Mantener sesión',
                confirmButtonColor: '#3085d6',
                cancelButtonText: 'Cerrar sesión',
                cancelButtonColor: '#d33',
                buttonsStyling: true,
                
                // Configurar tamaño y espaciado de botones
                customClass: {
                    confirmButton: 'btn btn-primary btn-lg mx-2',
                    cancelButton: 'btn btn-danger btn-lg mx-2',
                    popup: 'swal-wide'
                },
                
                // Prevenir cierre no intencional
                allowOutsideClick: false,
                allowEscapeKey: false,
                
                // Función a ejecutar cuando se abre el modal
                didOpen: (popup) => {
                    // Manejar eventos de hover para el timer
                    popup.addEventListener('mouseenter', Swal.stopTimer);
                    popup.addEventListener('mouseleave', Swal.resumeTimer);
                }
            };
            
            // Estilos adicionales para asegurar que los botones sean visibles
            const style = document.createElement('style');
            style.innerHTML = `
                .swal-wide {
                    min-width: 400px !important;
                }
                .swal2-confirm, .swal2-cancel {
                    min-width: 120px !important;
                    font-size: 1rem !important;
                    display: inline-block !important;
                    margin: 0.25rem !important;
                }
                .swal2-actions {
                    justify-content: center !important;
                    gap: 10px !important;
                }
            `;
            document.head.appendChild(style);
            
            // Mostrar el diálogo
            Swal.fire(swalConfig).then((result) => {
                warningShown = false; // Restablecer el estado
                
                if (result.isConfirmed) {
                    // Si el usuario decide mantener la sesión, reiniciar el temporizador
                    resetTimer();
                } else if (result.dismiss === Swal.DismissReason.cancel) {
                    // Si el usuario decide cerrar sesión manualmente
                    logout();
                } else if (result.dismiss === Swal.DismissReason.timer) {
                    // Si se agota el tiempo de advertencia, cerrar sesión
                    logout();
                }
                
                // Limpiar el estilo
                document.head.removeChild(style);
            });
        }
    }

    // Función para cerrar sesión
    function logout() {
        // Puesto que Django-allauth requiere un POST para el cierre de sesión
        // Creamos un formulario y lo enviamos
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = logoutUrl;
        
        // Añadir el token CSRF
        const csrfField = document.createElement('input');
        csrfField.type = 'hidden';
        csrfField.name = 'csrfmiddlewaretoken';
        csrfField.value = csrftoken;
        
        form.appendChild(csrfField);
        document.body.appendChild(form);
        form.submit();
    }

    // Eventos que reinician el temporizador de inactividad
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
    
    // Agregar eventos al documento
    events.forEach(function(event) {
        document.addEventListener(event, handleUserActivity, true);
    });
    
    // Verificar periódicamente si la inactividad ha expirado basado en todas las pestañas
    function checkInactivity() {
        const lastActivityTime = getLastActivityTime();
        const currentTime = Date.now();
        const inactiveTime = currentTime - lastActivityTime;
        
        if (inactiveTime >= (inactivityTime - 30000) && !warningShown) {
            // Si ha pasado el tiempo de inactividad menos 30 segundos, mostrar la advertencia
            showWarning();
        }
    }
    
    // Escuchar eventos de storage para sincronizar entre pestañas
    window.addEventListener('storage', function(event) {
        if (event.key === LAST_ACTIVITY_TIME_KEY) {
            // Si otra pestaña ha actualizado la hora de última actividad y no hay advertencia activa
            if (!warningShown) {
                resetTimer();
            }
        }
    });
    
    // Comprobar inactividad periódicamente
    setInterval(checkInactivity, CHECK_INTERVAL);

    // Iniciar el temporizador
    resetTimer();
}); 
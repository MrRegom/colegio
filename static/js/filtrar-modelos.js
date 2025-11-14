/**
 * JavaScript para filtrar modelos dinámicamente por marca
 * Se aplica a formularios de Artículos y Activos
 */
document.addEventListener('DOMContentLoaded', function() {
    const marcaSelect = document.getElementById('id_marca');
    const modeloSelect = document.getElementById('id_modelo');
    
    if (!marcaSelect || !modeloSelect) {
        return; // No hay campos de marca/modelo en esta página
    }
    
    // URL del endpoint AJAX
    const urlFiltrarModelos = '/inventario/ajax/filtrar-modelos/';
    
    // Función para cargar modelos según la marca seleccionada
    function cargarModelos(marcaId) {
        if (!marcaId) {
            // Si no hay marca seleccionada, deshabilitar y limpiar modelo
            modeloSelect.disabled = true;
            modeloSelect.innerHTML = '<option value="">Selecciona primero una marca</option>';
            return;
        }
        
        // Habilitar select de modelo
        modeloSelect.disabled = false;
        modeloSelect.innerHTML = '<option value="">Cargando...</option>';
        
        // Hacer petición AJAX
        fetch(`${urlFiltrarModelos}?marca_id=${marcaId}`)
            .then(response => response.json())
            .then(data => {
                modeloSelect.innerHTML = '<option value="">Selecciona un modelo</option>';
                
                if (data.length === 0) {
                    modeloSelect.innerHTML += '<option value="">No hay modelos disponibles para esta marca</option>';
                    return;
                }
                
                data.forEach(modelo => {
                    const option = document.createElement('option');
                    option.value = modelo.id;
                    option.textContent = `${modelo.codigo} - ${modelo.nombre}`;
                    modeloSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error al cargar modelos:', error);
                modeloSelect.innerHTML = '<option value="">Error al cargar modelos</option>';
            });
    }
    
    // Event listener para cambios en la marca
    marcaSelect.addEventListener('change', function() {
        cargarModelos(this.value);
    });
    
    // Si hay una marca seleccionada al cargar (modo edición), cargar sus modelos
    if (marcaSelect.value) {
        cargarModelos(marcaSelect.value);
    }
    
    // Auto-completar nombre de artículo
    const nombreArticuloSelect = document.getElementById('id_nombre_articulo');
    const nombreInput = document.getElementById('id_nombre');
    
    if (nombreArticuloSelect && nombreInput) {
        nombreArticuloSelect.addEventListener('change', function() {
            if (this.value) {
                const selectedOption = this.options[this.selectedIndex];
                const nombreArticulo = selectedOption.textContent.trim();
                
                // Actualizar el campo nombre con el nombre del artículo seleccionado
                if (!nombreInput.value || confirm('¿Desea reemplazar el nombre actual con el del catálogo?')) {
                    nombreInput.value = nombreArticulo;
                }
            }
        });
    }
});


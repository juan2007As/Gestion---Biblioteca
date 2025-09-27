// ========================================
// SISTEMA DE GESTIÓN DE USUARIOS - BIBLIOTECA
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // ===========================================
    // DECLARACIÓN DE ELEMENTOS DEL DOM
    // ===========================================
    const searchInput = document.getElementById('input__Busqueda');
    const tableBody = document.getElementById('tableBody');
    const rows = tableBody.getElementsByTagName('tr');
    
    // Botones principales
    const addUserButton = document.getElementById('Boton_Agregar');
    const deleteUserButton = document.getElementById('Boton_Eliminar');
    
    // Contenedores de formularios
    const addUserForm = document.getElementById('Box__contenedor_menu');
    const deleteUserForm = document.getElementById('Box__contenedor_Delete');
    const updateUserForm = document.getElementById('Box__contenedor_Actualizar');
    
    // Formularios
    const addForm = document.querySelector('#Agregar_usuario_menu form');

    // ===========================================
    // FUNCIONALIDAD DE BÚSQUEDA
    // ===========================================
    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value.toLowerCase();
        for (let i = 0; i < rows.length; i++) {
            const text = rows[i].textContent.toLowerCase();
            rows[i].style.display = text.includes(searchTerm) ? '' : 'none';
        }
    });

    // ===========================================
    // MANEJO DE FORMULARIOS (MOSTRAR/OCULTAR)
    // ===========================================
    
    // Función auxiliar para ocultar todos los formularios
    function ocultarTodosLosFormularios() {
        addUserForm.style.display = 'none';
        deleteUserForm.style.display = 'none';
        updateUserForm.style.display = 'none';
    }

    // Mostrar/ocultar formulario de agregar usuario
    addUserButton.addEventListener('click', function() {
        if (addUserForm.style.display === 'none' || addUserForm.style.display === '') {
            ocultarTodosLosFormularios();
            addUserForm.style.display = 'block';
        } else {
            addUserForm.style.display = 'none';
        }
    });

    // Mostrar/ocultar formulario de eliminar usuario
    deleteUserButton.addEventListener('click', function() {
        if (deleteUserForm.style.display === 'none' || deleteUserForm.style.display === '') {
            ocultarTodosLosFormularios();
            deleteUserForm.style.display = 'block';
        } else {
            deleteUserForm.style.display = 'none';
        }
    });

    // ===========================================
    // MANEJO DE BOTONES DE ACTUALIZAR EN TABLA
    // ===========================================
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-actualizar')) {
            const usuarioDocumento = e.target.getAttribute('data-usuario-documento');
            if (usuarioDocumento) {
                mostrarMenuActualizar(usuarioDocumento);
            }
        }
    });

    // ===========================================
    // VALIDACIONES DE FORMULARIOS
    // ===========================================
    addForm.addEventListener('submit', function(e) {
        const email = document.querySelector('#Agregar_usuario_menu input[name="email"]').value;
        const telefono = document.querySelector('#Agregar_usuario_menu input[name="telefono"]').value;
        
        // Validar formato de email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            e.preventDefault();
            alert('Por favor, ingrese un email válido.');
            return;
        }
        
        // Validar que el teléfono solo contenga números
        if (!/^\d+$/.test(telefono)) {
            e.preventDefault();
            alert('El teléfono debe contener solo números.');
            return;
        }
    });
});

// ===========================================
// FUNCIONES PARA MANEJO DEL MENÚ DE ACTUALIZAR
// ===========================================

/**
 * Muestra el menú de actualizar con los datos del usuario seleccionado
 * @param {string} documentoUsuario - Documento del usuario a actualizar
 */
function mostrarMenuActualizar(documentoUsuario) {
    // Obtener elementos del DOM
    const updateUserForm = document.getElementById('Box__contenedor_Actualizar');
    const addUserForm = document.getElementById('Box__contenedor_menu');
    const deleteUserForm = document.getElementById('Box__contenedor_Delete');
    
    // Ocultar otros formularios
    addUserForm.style.display = 'none';
    deleteUserForm.style.display = 'none';
    
    // Buscar los datos del usuario en la tabla
    const usuarioData = obtenerDatosUsuarioDeLaTabla(documentoUsuario);
    
    if (usuarioData) {
        llenarFormularioActualizar(usuarioData);
        updateUserForm.style.display = 'block';
    } else {
        alert('No se pudieron cargar los datos del usuario.');
    }
}

/**
 * Obtiene los datos de un usuario desde la tabla HTML
 * @param {string} documentoUsuario - Documento del usuario a buscar
 * @returns {Object|null} - Datos del usuario o null si no se encuentra
 */
function obtenerDatosUsuarioDeLaTabla(documentoUsuario) {
    const filas = document.querySelectorAll('#tableBody tr');
    
    for (let fila of filas) {
        const documentoEnTabla = fila.cells[0].textContent;
        if (documentoEnTabla === documentoUsuario) {
            return {
                documento: documentoEnTabla,
                nombre: fila.cells[1].textContent,
                apellido: fila.cells[2].textContent,
                telefono: fila.cells[3].textContent,
                email: fila.cells[4].textContent,
                rol: fila.cells[5].textContent
            };
        }
    }
    return null;
}

/**
 * Llena el formulario de actualizar con los datos del usuario
 * @param {Object} usuarioData - Datos del usuario
 */
function llenarFormularioActualizar(usuarioData) {
    document.getElementById('documento_usuario_actualizar').value = usuarioData.documento;
    document.getElementById('nombre_actualizar').value = usuarioData.nombre;
    document.getElementById('apellido_actualizar').value = usuarioData.apellido;
    document.getElementById('telefono_actualizar').value = usuarioData.telefono;
    document.getElementById('email_actualizar').value = usuarioData.email;
    
    // Configurar el rol
    const rolSelect = document.getElementById('rol_actualizar');
    if (usuarioData.rol === 'admin') {
        rolSelect.value = 'admin';
    } else if (usuarioData.rol === 'normal') {
        rolSelect.value = 'normal';
    } else {
        rolSelect.value = '';
    }
}

/**
 * Oculta el menú de actualizar y limpia el formulario
 */
function ocultarMenuActualizar() {
    const updateUserForm = document.getElementById('Box__contenedor_Actualizar');
    updateUserForm.style.display = 'none';
    
    // Limpiar todos los campos del formulario
    const campos = [
        'id_usuario_actualizar',
        'nombre_actualizar', 
        'apellido_actualizar',
        'telefono_actualizar',
        'email_actualizar',
        'rol_actualizar'
    ];
    
    campos.forEach(campo => {
        const elemento = document.getElementById(campo);
        if (elemento) {
            elemento.value = '';
        }
    });
}
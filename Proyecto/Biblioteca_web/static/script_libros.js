// ========================================
// SISTEMA DE GESTIÓN DE LIBROS - BIBLIOTECA
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // ===========================================
    // DECLARACIÓN DE ELEMENTOS DEL DOM
    // ===========================================
    const searchInput = document.getElementById('input__Busqueda');
    const tableBody = document.getElementById('tableBody');
    const rows = tableBody.getElementsByTagName('tr');
    
    // Botones principales
    const addBookButton = document.getElementById('Boton_Agregar');
    const deleteBookButton = document.getElementById('Boton_Eliminar');
    
    // Contenedores de formularios
    const addBookForm = document.getElementById('Box__contenedor_menu');
    const deleteBookForm = document.getElementById('Box__contenedor_Delete');
    const updateBookForm = document.getElementById('Box__contenedor_Actualizar');
    
    // Formularios
    const addForm = document.querySelector('#Agregar_libro_menu form');

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
        addBookForm.style.display = 'none';
        deleteBookForm.style.display = 'none';
        updateBookForm.style.display = 'none';
    }

    // Mostrar/ocultar formulario de agregar libro
    addBookButton.addEventListener('click', function() {
        if (addBookForm.style.display === 'none' || addBookForm.style.display === '') {
            ocultarTodosLosFormularios();
            addBookForm.style.display = 'block';
        } else {
            addBookForm.style.display = 'none';
        }
    });

    // Mostrar/ocultar formulario de eliminar libro
    deleteBookButton.addEventListener('click', function() {
        if (deleteBookForm.style.display === 'none' || deleteBookForm.style.display === '') {
            ocultarTodosLosFormularios();
            deleteBookForm.style.display = 'block';
        } else {
            deleteBookForm.style.display = 'none';
        }
    });

    // ===========================================
    // MANEJO DE BOTONES DE ACTUALIZAR EN TABLA
    //      ===========================================
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-actualizar')) {
            const libroId = parseInt(e.target.getAttribute('data-libro-id'));
            if (libroId) {
                mostrarMenuActualizar(libroId);
            }
        }
    });

    // ===========================================
    // VALIDACIONES DE FORMULARIOS
    // ===========================================
    addForm.addEventListener('submit', function(e) {
        const año = document.querySelector('#Agregar_libro_menu input[name="año"]').value;
        if (!año || isNaN(año) || año < 0 || año > 2025) {
            e.preventDefault();
            alert('El año debe ser un número válido entre 0 y 2025.');
        }
    });
});

// ===========================================
// FUNCIONES PARA MANEJO DEL MENÚ DE ACTUALIZAR
// ===========================================

/**
 * Muestra el menú de actualizar con los datos del libro seleccionado
 * @param {number} idLibro - ID del libro a actualizar
 */
function mostrarMenuActualizar(idLibro) {
    // Obtener elementos del DOM
    const updateBookForm = document.getElementById('Box__contenedor_Actualizar');
    const addBookForm = document.getElementById('Box__contenedor_menu');
    const deleteBookForm = document.getElementById('Box__contenedor_Delete');
    
    // Ocultar otros formularios
    addBookForm.style.display = 'none';
    deleteBookForm.style.display = 'none';
    
    // Buscar los datos del libro en la tabla
    const libroData = obtenerDatosLibroDeLaTabla(idLibro);
    
    if (libroData) {
        llenarFormularioActualizar(libroData);
        updateBookForm.style.display = 'block';
    } else {
        alert('No se pudieron cargar los datos del libro.');
    }
}

/**
 * Obtiene los datos de un libro desde la tabla HTML
 * @param {number} idLibro - ID del libro a buscar
 * @returns {Object|null} - Datos del libro o null si no se encuentra
 */
function obtenerDatosLibroDeLaTabla(idLibro) {
    const filas = document.querySelectorAll('#tableBody tr');
    
    for (let fila of filas) {
        const idEnTabla = parseInt(fila.cells[0].textContent);
        if (idEnTabla === idLibro) {
            return {
                id: idEnTabla,
                titulo: fila.cells[1].textContent,
                autor: fila.cells[2].textContent,
                editorial: fila.cells[3].textContent,
                año: fila.cells[4].textContent,
                genero: fila.cells[5].textContent,
                disponible: fila.cells[6].textContent
            };
        }
    }
    return null;
}

/**
 * Llena el formulario de actualizar con los datos del libro
 * @param {Object} libroData - Datos del libro
 */
function llenarFormularioActualizar(libroData) {
    document.getElementById('id_libro_actualizar').value = libroData.id;
    document.getElementById('titulo_actualizar').value = libroData.titulo;
    document.getElementById('autor_actualizar').value = libroData.autor;
    document.getElementById('editorial_actualizar').value = libroData.editorial;
    document.getElementById('año_actualizar').value = libroData.año;
    document.getElementById('genero_actualizar').value = libroData.genero;
    
    // Configurar la disponibilidad
    const disponibleSelect = document.getElementById('disponible_actualizar');
    if (libroData.disponible === 'Sí') {
        disponibleSelect.value = 'si';
    } else if (libroData.disponible === 'No') {
        disponibleSelect.value = 'no';
    } else {
        disponibleSelect.value = '';
    }
}

/**
 * Oculta el menú de actualizar y limpia el formulario
 */
function ocultarMenuActualizar() {
    const updateBookForm = document.getElementById('Box__contenedor_Actualizar');
    updateBookForm.style.display = 'none';
    
    // Limpiar todos los campos del formulario
    const campos = [
        'id_libro_actualizar',
        'titulo_actualizar', 
        'autor_actualizar',
        'editorial_actualizar',
        'año_actualizar',
        'genero_actualizar',
        'disponible_actualizar'
    ];
    
    campos.forEach(campo => {
        const elemento = document.getElementById(campo);
        if (elemento) {
            elemento.value = '';
        }
    });
}
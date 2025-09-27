// ========================================
// LISTA DE PRÉSTAMOS - BIBLIOTECA
// Archivo: script_prestamos.js
// Funcionalidad: Solo visualización y búsqueda
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // ===========================================
    // DECLARACIÓN DE ELEMENTOS DEL DOM
    // ===========================================
    const searchInput = document.getElementById('input__Busqueda');
    const tableBody = document.getElementById('tableBody');
    const rows = tableBody.getElementsByTagName('tr');
    const PrestamoBtn = document.getElementById('Boton_Prestamo');
    const PrestamoForm = document.getElementById('Box__contenedor_prestamo');

    // ===========================================
    // FUNCIONALIDAD DE BÚSQUEDA
    // ===========================================
    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value.toLowerCase();
        
        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            
            // Saltar la fila de "no hay préstamos"
            if (row.querySelector('.no-prestamos')) {
                continue;
            }
            
            const text = row.textContent.toLowerCase();
            
            // Mostrar/ocultar fila según coincidencia
            if (text.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
        
        // Contar filas visibles
        updateVisibleCount();
    });

    // ===========================================
    // ACTUALIZAR CONTADOR DE RESULTADOS
    // ===========================================
    function updateVisibleCount() {
        let visibleCount = 0;
        
        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            
            // Saltar la fila de "no hay préstamos"
            if (row.querySelector('.no-prestamos')) {
                continue;
            }
            
            if (row.style.display !== 'none') {
                visibleCount++;
            }
        }
        
        // Actualizar el título con el contador si hay búsqueda activa
        const title = document.querySelector('.Administracion__title');
        const searchTerm = searchInput.value.trim();
        
        if (searchTerm) {
            title.textContent = `Lista de préstamos: ${visibleCount} resultado(s) encontrado(s)`;
        } else {
            title.textContent = 'Lista de préstamos:';
        }
    }

    // ===========================================
    // FUNCIONALIDADES ADICIONALES
    // ===========================================
    
    // Resaltar términos de búsqueda (opcional)
    function highlightSearchTerm(text, term) {
        if (!term) return text;
        
        const regex = new RegExp(`(${term})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    // Estadísticas en tiempo real
    function updateStatistics() {
        const allRows = Array.from(rows).filter(row => !row.querySelector('.no-prestamos'));
        const activeRows = Array.from(rows).filter(row => 
            !row.querySelector('.no-prestamos') && 
            row.querySelector('.estado-activo')
        );
        const returnedRows = Array.from(rows).filter(row => 
            !row.querySelector('.no-prestamos') && 
            row.querySelector('.estado-devuelto')
        );
        
        // Actualizar estadísticas si existen los elementos
        const totalStat = document.querySelector('.stat-box:nth-child(1) .stat-numero');
        const activeStat = document.querySelector('.stat-box:nth-child(2) .stat-numero');
        const returnedStat = document.querySelector('.stat-box:nth-child(3) .stat-numero');
        
        if (totalStat) totalStat.textContent = allRows.length;
        if (activeStat) activeStat.textContent = activeRows.length;
        if (returnedStat) returnedStat.textContent = returnedRows.length;
    }
    
    // Ejecutar estadísticas al cargar
    updateStatistics();
    
    // ===========================================
    // EFECTOS VISUALES
    // ===========================================
    
    // Hover effect para filas
    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        
        if (!row.querySelector('.no-prestamos')) {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#e9ecef';
            });
            
            row.addEventListener('mouseleave', function() {
                // Restaurar color original según fila par/impar
                if (i % 2 === 0) {
                    this.style.backgroundColor = '#f9f9f9';
                } else {
                    this.style.backgroundColor = 'white';
                }
            });
        }
    }
    
    // ===========================================
    // FUNCIONALIDAD DE EXPORTAR (OPCIONAL)
    // ===========================================
    
    // Función para exportar datos visibles a CSV
    function exportToCSV() {
        const visibleRows = Array.from(rows).filter(row => 
            !row.querySelector('.no-prestamos') && 
            row.style.display !== 'none'
        );
        
        let csv = 'ID Préstamo,Usuario,Libro,Fecha Préstamo,Fecha Esperada,Fecha Real,Estado,Multa\n';
        
        visibleRows.forEach(row => {
            const cells = row.getElementsByTagName('td');
            const rowData = Array.from(cells).map(cell => 
                `"${cell.textContent.trim().replace(/"/g, '""')}"`
            ).join(',');
            csv += rowData + '\n';
        });
        
        // Crear y descargar archivo
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'prestamos_lista.csv';
        a.click();
        window.URL.revokeObjectURL(url);
    }
    
    // Si existe un botón de exportar, agregar funcionalidad
    const exportButton = document.getElementById('btn-exportar');
    if (exportButton) {
        exportButton.addEventListener('click', exportToCSV);
    }
});
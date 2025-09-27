// crea la funcionalidad completa para abrir y cerrar el menu de prestamos
document.addEventListener('DOMContentLoaded', function() {
    const PrestamoBtn = document.getElementById('Boton_Prestamo');
    const PrestamoForm = document.getElementById('Box__contenedor_prestamo');

        PrestamoBtn.addEventListener('click', function() {
            if (PrestamoForm.style.display === 'none' || PrestamoForm.style.display === '') {
                PrestamoForm.style.display = 'block';
            } else {
                PrestamoForm.style.display = 'none';
            }
        });
    });

document.addEventListener('DOMContentLoaded', function() {
    const DevolverBtn = document.getElementById('Boton_Devolver');
    const DevolverForm = document.getElementById('Box__contenedor_devolver');

        DevolverBtn.addEventListener('click', function() {
            if (DevolverForm.style.display === 'none' || DevolverForm.style.display === '') {
                DevolverForm.style.display = 'block';
            } else {
                DevolverForm.style.display = 'none';
            }
        });
});
document.addEventListener('DOMContentLoaded', function() {
    const apiUrl = 'http://192.168.0.34:5000/api/motos?sucursal=1';
    const tableBody = document.querySelector('#inventory-table tbody');

    function loadInventory() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(motos => {
                console.log('Motos recibidas:', motos);  // Verifica la estructura de los datos
                tableBody.innerHTML = '';  // Limpia la tabla antes de cargar los datos
                motos.forEach(moto => {
                    console.log('Moto procesada:', moto);  // Verifica cada moto
                    const modelo = moto.modelo || 'Modelo no disponible';
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${moto.id_moto}</td>
                        <td>${modelo}</td>
                        <td>${moto.marca || 'Marca no disponible'}</td>
                        <td><img src="data:image/jpeg;base64,${moto.diseno_jpg || ''}" alt="${modelo}" width="100"></td>
                        <td>
                            <button class="edit-button" data-id="${moto.id_moto}">Editar</button>
                            <button class="delete-button" data-id="${moto.id_moto}">Eliminar</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
                attachEventListeners();  // Añadir los eventos después de cargar los datos
            })
            .catch(error => {
                console.error('Error loading inventory:', error);
                alert('Hubo un error al cargar el inventario');
            });
    }

    function attachEventListeners() {
        document.querySelectorAll('.edit-button').forEach(button => {
            button.addEventListener('click', function() {
                const idMoto = this.getAttribute('data-id');
                window.location.href = `agregar_moto.html?id=${idMoto}`;
            });
        });

        document.querySelectorAll('.delete-button').forEach(button => {
            button.addEventListener('click', function() {
                const idMoto = this.getAttribute('data-id');
                if (confirm('¿Estás seguro de que deseas eliminar esta moto?')) {
                    fetch(`http://192.168.0.34:5000/api/motos/${idMoto}`, {
                        method: 'DELETE'
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert('Moto eliminada correctamente');
                        loadInventory();  // Recargar el inventario después de la eliminación
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Hubo un error al eliminar la moto');
                    });
                }
            });
        });
    }

    loadInventory();  // Cargar el inventario cuando la página esté lista
});

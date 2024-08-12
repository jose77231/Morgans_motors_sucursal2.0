document.addEventListener('DOMContentLoaded', function() {
    const selectElement = document.getElementById('select');
    const headerTitle = document.getElementById('header-title');
    const searchInput = document.getElementById('search-input');
    let motosData = [];

    // Función para cargar las motos desde la API
    function loadMotos(url) {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                motosData = data; // Almacenar las motos en la variable global
                displayMotos(motosData);
            })
            .catch(error => console.error('Error al cargar las motos:', error));
    }

    // Función para mostrar las motos
    function displayMotos(motos) {
        const container = document.getElementById('moto-container');
        container.innerHTML = ''; // Limpiar el contenedor antes de cargar nuevas motos
        motos.forEach(moto => {
            const card = document.createElement('div');
            card.classList.add('card');

            // Crear la imagen
            const img = document.createElement('img');
            img.src = 'data:image/jpeg;base64,' + (moto.diseno_jpg || '');
            card.appendChild(img);

            // Crear el contenido de la tarjeta
            const content = document.createElement('div');
            content.classList.add('card-content');

            // Título con la marca y el modelo
            const title = document.createElement('h3');
            title.textContent = `${moto.marca || 'Marca desconocida'} ${moto.modelo || ''}`;
            content.appendChild(title);

            // Detalles adicionales
            const details = document.createElement('p');
            details.textContent = `${moto.tipo_cilindraje || ''} - ${moto.ano || ''}`;
            content.appendChild(details);

            // Añadir contenido a la tarjeta
            card.appendChild(content);
            container.appendChild(card);
        });
    }

    // Función para actualizar el título del header
    function updateHeaderTitle() {
        const selectedOption = selectElement.options[selectElement.selectedIndex].text;
        headerTitle.textContent = selectedOption;
    }

    // Función para filtrar las motos por búsqueda
    function filterMotos(query) {
        const filteredMotos = motosData.filter(moto => {
            const marcaModelo = `${moto.marca || ''} ${moto.modelo || ''}`.toLowerCase();
            return marcaModelo.includes(query.toLowerCase());
        });
        displayMotos(filteredMotos);
    }

    // Cargar las motos al inicio usando la opción seleccionada
    loadMotos(selectElement.value);
    updateHeaderTitle();

    // Escuchar cambios en el select para cargar las motos correspondientes y cambiar el título
    selectElement.addEventListener('change', function() {
        loadMotos(selectElement.value);
        updateHeaderTitle();
    });

    // Escuchar cambios en el campo de búsqueda para filtrar las motos
    searchInput.addEventListener('input', function() {
        filterMotos(searchInput.value);
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('moto-form');
    const idMotoInput = document.getElementById('id_moto');
    const apiUrl = 'http://192.168.0.34:5000/api/motos';
    let selectedImage = '';

    // Verifica si estamos editando una moto
    const params = new URLSearchParams(window.location.search);
    const idMoto = params.get('id');
    if (idMoto) {
        fetch(`${apiUrl}/${idMoto}`)
            .then(response => response.json())
            .then(data => {
                // Autocompletar el formulario con los datos de la moto
                idMotoInput.value = data.id_moto;
                document.getElementById('id_producto').value = data.id_producto;
                document.getElementById('modelo').value = data.modelo;
                document.getElementById('marca').value = data.marca;
                document.getElementById('tipo_cilindraje').value = data.tipo_cilindraje;
                document.getElementById('freno_trasero').value = data.freno_trasero;
                document.getElementById('freno_delantero').value = data.freno_delantero;
                document.getElementById('numero_serie').value = data.numero_serie;
                document.getElementById('ano').value = data.ano;
                document.getElementById('garantia_servicio').value = data.garantia_servicio;
                document.getElementById('tamano_peso').value = data.tamano_peso;
                document.getElementById('motor').value = data.motor;
                document.getElementById('transmision').value = data.transmision;
                document.getElementById('potencia').value = data.potencia;
                selectedImage = data.diseno_jpg || '';
            });
    }

    // Convertir la imagen seleccionada a base64
    document.getElementById('diseno_jpg').addEventListener('change', function(event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onloadend = function() {
            selectedImage = reader.result.split(',')[1]; // Extrae solo la parte base64
        };

        if (file) {
            reader.readAsDataURL(file);
        }
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const motoData = {
            id_moto: idMotoInput.value || null,
            id_producto: document.getElementById('id_producto').value,
            modelo: document.getElementById('modelo').value,
            marca: document.getElementById('marca').value,
            tipo_cilindraje: document.getElementById('tipo_cilindraje').value,
            freno_trasero: document.getElementById('freno_trasero').value,
            freno_delantero: document.getElementById('freno_delantero').value,
            numero_serie: document.getElementById('numero_serie').value,
            ano: document.getElementById('ano').value,
            diseno_jpg: selectedImage,  // Usa la imagen seleccionada
            garantia_servicio: document.getElementById('garantia_servicio').value,
            tamano_peso: document.getElementById('tamano_peso').value,
            motor: document.getElementById('motor').value,
            transmision: document.getElementById('transmision').value,
            potencia: document.getElementById('potencia').value,
            id_sucursal: 1  // Fijar el ID de la sucursal en 1
        };

        const method = idMoto ? 'PUT' : 'POST';
        const url = idMoto ? `${apiUrl}/${idMoto}` : apiUrl;

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(motoData)
        })
        .then(response => response.json())
        .then(data => {
            alert('Moto guardada correctamente');
            window.location.href = 'inventario.html';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un error al guardar la moto');
        });
    });
});

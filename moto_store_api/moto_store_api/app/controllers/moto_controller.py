from flask import request, jsonify
from app.database.connection import create_connection
import base64
from mysql.connector import Error
import re

def get_motos():
    sucursal_id = request.args.get('sucursal', type=int)
    
    connection = create_connection()
    if connection is None:
        return jsonify({'message': 'Error de conexión a la base de datos'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        if sucursal_id:
            cursor.execute("SELECT * FROM motos WHERE id_sucursal = %s", (sucursal_id,))
        else:
            cursor.execute("SELECT * FROM motos")
        
        motos = cursor.fetchall()
        for moto in motos:
            for key, value in moto.items():
                if isinstance(value, bytes):
                    moto[key] = base64.b64encode(value).decode('utf-8')
    except Error as e:
        return jsonify({'message': f'Error: {e}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(motos), 200

def get_moto_by_id(id_moto):
    connection = create_connection()
    if connection is None:
        return jsonify({'message': 'Error de conexión a la base de datos'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM motos WHERE id_moto = %s", (id_moto,))
        moto = cursor.fetchone()
        if moto:
            for key, value in moto.items():
                if isinstance(value, bytes):
                    moto[key] = base64.b64encode(value).decode('utf-8')
    except Error as e:
        return jsonify({'message': f'Error: {e}'}), 500
    finally:
        cursor.close()
        connection.close()

    if moto:
        return jsonify(moto), 200
    else:
        return jsonify({'message': 'Moto no encontrada'}), 404

def create_moto():
    data = request.get_json()
    connection = create_connection()
    if connection is None:
        return jsonify({'message': 'Error de conexión a la base de datos'}), 500

    try:
        cursor = connection.cursor()

        # Asegurarse de que la cadena de base64 tiene el padding correcto
        base64_image = data.get('diseno_jpg', '')
        base64_image = re.sub(r'[^A-Za-z0-9+/=]', '', base64_image)  # Eliminar caracteres no válidos
        base64_image += '=' * (-len(base64_image) % 4)  # Añadir el padding correcto

        # Consulta SQL ajustada, con campos y valores que coinciden
        sql = """INSERT INTO motos (id_moto, id_producto, modelo, marca, tipo_cilindraje, freno_trasero, 
                freno_delantero, numero_serie, ano, diseno_jpg, garantia_servicio, 
                tamano_peso, motor, transmision, potencia, id_sucursal) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        values = (
            data.get('id_moto'),
            data.get('id_producto'),  # Asegúrate de que este ID existe en la tabla `producto`
            data.get('modelo'),
            data.get('marca'),
            data.get('tipo_cilindraje'),
            data.get('freno_trasero'),
            data.get('freno_delantero'),
            data.get('numero_serie'),
            data.get('ano'),
            base64.b64decode(base64_image) if base64_image else None,
            data.get('garantia_servicio'),
            data.get('tamano_peso'),
            data.get('motor'),
            data.get('transmision'),
            data.get('potencia'),
            data.get('id_sucursal')
        )
        
        cursor.execute(sql, values)
        connection.commit()
    except Error as e:
        if e.errno == 1062:
            return jsonify({'message': 'El ID ya está ocupado, usa otro ID para este producto'}), 400
        return jsonify({'message': f'Error: {e}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Moto agregada correctamente'}), 201

def update_moto(id_moto):
    data = request.get_json()
    connection = create_connection()
    if connection is None:
        return jsonify({'message': 'Error de conexión a la base de datos'}), 500

    try:
        cursor = connection.cursor()

        # Decodificar la imagen si está presente
        diseno_jpg_data = base64.b64decode(data['diseno_jpg']) if 'diseno_jpg' in data and data['diseno_jpg'] else None

        # Consulta de actualización
        sql = """UPDATE motos SET modelo = %s, id_producto = %s, marca = %s, tipo_cilindraje = %s, freno_trasero = %s, 
                freno_delantero = %s, numero_serie = %s, ano = %s, diseno_jpg = %s, 
                garantia_servicio = %s, tamano_peso = %s, motor = %s, 
                transmision = %s, potencia = %s, id_sucursal = %s WHERE id_moto = %s"""
        values = (
            data['modelo'], 
            data.get('id_producto'),  # Asegúrate de que este ID existe en la tabla `producto`
            data['marca'], 
            data['tipo_cilindraje'], 
            data['freno_trasero'], 
            data['freno_delantero'], 
            data['numero_serie'], 
            data['ano'], 
            diseno_jpg_data, 
            data['garantia_servicio'], 
            data['tamano_peso'], 
            data['motor'], 
            data['transmision'], 
            data['potencia'], 
            data['id_sucursal'], 
            id_moto
        )

        cursor.execute(sql, values)
        connection.commit()
    except Error as e:
        return jsonify({'message': f'Error: {e}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Moto actualizada correctamente'}), 200


def delete_moto(id_moto):
    connection = create_connection()
    if connection is None:
        return jsonify({'message': 'Error de conexión a la base de datos'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM motos WHERE id_moto = %s", (id_moto,))
        connection.commit()
    except Error as e:
        return jsonify({'message': f'Error: {e}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Moto eliminada correctamente'}), 200

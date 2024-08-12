from flask import request, jsonify
from app.database.connection import create_connection
from mysql.connector import Error  # Importar Error
import bcrypt  # Importar bcrypt


def login_usuario():
    data = request.get_json()
    correo_electronico = data.get('correo_electronico')
    contrasena = data.get('contrasena')
    
    connection = create_connection()
    if connection is None:
        return jsonify({'success': False, 'message': 'Error de conexión a la base de datos'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id_sucursal, contrasena FROM usuario WHERE correo_electronico = %s", (correo_electronico,))
        usuario = cursor.fetchone()
    except Error as e:
        return jsonify({'success': False, 'message': f'Error: {e}'}), 500
    finally:
        cursor.close()
        connection.close()

    if usuario and bcrypt.checkpw(contrasena.encode('utf-8'), usuario['contrasena'].encode('utf-8')):
        return jsonify({'success': True, 'sucursal_id': usuario['id_sucursal']}), 200
    else:
        return jsonify({'success': False, 'message': 'Credenciales incorrectas'}), 401
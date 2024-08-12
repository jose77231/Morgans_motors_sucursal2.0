import mysql.connector
from mysql.connector import Error
import bcrypt

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='bd_tienda_motos',
            user='root',
            password=''
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def is_hashed(password):
    # Verifica si la contraseña ya está en formato bcrypt
    return password.startswith('$2b$') or password.startswith('$2a$') or password.startswith('$2y$')

def hash_passwords():
    connection = create_connection()
    if connection is None:
        print("Error de conexión a la base de datos")
        return

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, contrasena FROM usuario")  # Asegúrate de que el nombre de la tabla es correcto
        users = cursor.fetchall()

        for user in users:
            if not is_hashed(user['contrasena']):
                hashed_password = bcrypt.hashpw(user['contrasena'].encode('utf-8'), bcrypt.gensalt())
                update_sql = "UPDATE usuario SET contrasena = %s WHERE id = %s"
                cursor.execute(update_sql, (hashed_password.decode('utf-8'), user['id']))

        connection.commit()
        print("Contraseñas actualizadas correctamente")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    hash_passwords()

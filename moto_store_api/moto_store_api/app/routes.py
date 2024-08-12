from app.controllers.moto_controller import get_motos, get_moto_by_id, create_moto, update_moto, delete_moto
from app.controllers.usuario_controller import login_usuario  # Importa el controlador de login
from flask import Blueprint

def register_routes(app):
    moto_bp = Blueprint('motos', __name__)

    # Registrar las rutas de las motos
    moto_bp.route('/api/motos', methods=['GET'])(get_motos)
    moto_bp.route('/api/motos/<int:id_moto>', methods=['GET'])(get_moto_by_id)
    moto_bp.route('/api/motos', methods=['POST'])(create_moto)
    moto_bp.route('/api/motos/<int:id_moto>', methods=['PUT'])(update_moto)
    moto_bp.route('/api/motos/<int:id_moto>', methods=['DELETE'])(delete_moto)

    # Registrar la ruta de login
    moto_bp.route('/api/login', methods=['POST'])(login_usuario)

    app.register_blueprint(moto_bp)

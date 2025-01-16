from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/')
def index():
    response = {
        "success": True,
        "message": "Data received successfully",
    }
    return jsonify(response), 200


@api_bp.route('/databases/add', methods=['POST'])
def add_database():
    from web.flask.utils.models.database import create_database

    success, message = create_database(request)

    return jsonify({
        "success": success,
        "message": message,
    }), 200


@api_bp.route('/databases/check-connection/<int:database_id>', methods=['GET'])
def check_db_connection(database_id):
    from web.flask.databases.models import Database
    from web.flask.utils.common import model_to_dict
    from web.flask.utils.models.database import check_database_connection

    database = Database.query.filter_by(id=database_id).first()
    if not database:
        response = {
            "success": False,
            "message": "Database not found.",
        }
        return jsonify(response), 404

    database_dict = model_to_dict(database)

    success, message = check_database_connection(database_dict)
    response = {
        "success": success,
        "message": message,
    }
    return jsonify(response), 200

@api_bp.route('/databases/delete/<int:database_id>', methods=['POST'])
def remove_database(database_id):
    from web.flask.utils.models.database import delete_database

    success, message = delete_database(database_id)

    return jsonify({
        "success": success,
        "message": message,
    }), 200

@api_bp.route('/databases/list', methods=['GET'])
def database_list():
    from web.flask.utils.models.database import get_database_list
    type_param = request.args.get('type', '')
    data = get_database_list(type_param)

    response = {
        "success": True,
        "message": "Data received successfully",
        "data": data,
    }
    return jsonify(response), 200

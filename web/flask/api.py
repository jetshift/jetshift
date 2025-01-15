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
    data = request.get_json()

    host = data.get("host")
    password = data.get('password')

    response = {
        "success": True,
        "message": "Data received successfully",
        "host": host,
        "password": password,
    }

    return jsonify(response), 200


@api_bp.route('/databases/list', methods=['GET'])
def database_list():
    from web.flask.databases.models import Database

    type_param = request.args.get('type', '')
    all_databases = Database.query.filter_by(type=type_param)

    data = [
        {
            "id": db_entry.id,
            "type": db_entry.type,
            "name": db_entry.name,
            "host": db_entry.host,
            "port": db_entry.port,
            "user": db_entry.user,
            "database": db_entry.database,
            "engine": db_entry.engine,
            "status": db_entry.status,
            "created_at": db_entry.created_at.isoformat(),
            "updated_at": db_entry.updated_at.isoformat(),
        }
        for db_entry in all_databases
    ]

    response = {
        "success": True,
        "message": "Data received successfully",
        "data": data,
    }
    return jsonify(response), 200

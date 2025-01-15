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
    data = [
        {
            "id": 1,
            "name": "Database 1",
            "host": "localhost",
            "port": 5432,
            "user": "admin",
            "password": "securepass",
            "type": "postgres",
            "status": "active",
            "created_at": "2022-09-01T12:00:00Z",
            "updated_at": "2023-09-01T15:30:00Z"
        },
        {
            "id": 2,
            "name": "Database 2",
            "host": "remotehost.com",
            "port": 3306,
            "user": "readonlyuser",
            "password": "securereadonlypass",
            "type": "mysql",
            "status": "inactive",
            "created_at": "2022-09-15T08:00:00Z",
            "updated_at": "2023-10-01T12:30:00Z"
        }
    ]

    response = {
        "success": True,
        "message": "Data received successfully",
        "data": data,
    }
    return jsonify(response), 200

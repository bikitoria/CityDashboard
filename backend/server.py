# Filename - server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import (
    init_db,
    get_or_create_user,
    save_project,
    get_user_projects,
    load_project
)
from database.users import get_all_users
from buildingData.data_loader import buildings_data_list
from buildingData.process_data import simplify_building
from llm_service import parse_query, building_matches  # ✅ ADD THIS

app = Flask(__name__)
CORS(app)
init_db()

@app.route("/api/buildings")
def get_buildings():
    return jsonify(buildings_data_list)

@app.route("/api/query", methods=["POST"])
def query():
    try:
        user_input = request.json.get("text", "")
        filters = parse_query(user_input)
        print("Parsed filters:", filters)
        filtered = [b for b in buildings_data_list if building_matches(b, filters)]
        return jsonify(filtered)
    except Exception as e:
        import traceback
        print("Error in /api/query:", e)
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "").strip()
    if not username:
        return jsonify({"error": "Username is required."}), 400
    user_id = get_or_create_user(username)
    return jsonify({"message": "Login successful", "user_id": user_id}), 200

@app.route("/api/save", methods=["POST"])
def save():
    data = request.get_json()
    username = data.get("username")
    project_name = data.get("projectName")
    filters = data.get("filters")

    if not all([username, project_name, filters]):
        return jsonify({"error": "Missing data."}), 400

    user_id = get_or_create_user(username)
    save_project(user_id, project_name, filters)
    return jsonify({"message": "Project saved."}), 200

@app.route("/api/projects", methods=["GET"])
def list_projects():
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify({"error": "Username required."}), 400

    user_id = get_or_create_user(username)
    projects = get_user_projects(user_id)
    return jsonify([{"id": pid, "name": name} for pid, name in projects])

@app.route("/api/project/<int:project_id>", methods=["GET"])
def load(project_id):
    filters = load_project(project_id)
    if filters is None:
        return jsonify({"error": "Project not found."}), 404
    return jsonify({"filters": filters})

@app.route("/api/users", methods=["GET"])
def list_users():
    return jsonify(get_all_users())

if __name__ == '__main__':
    app.run()

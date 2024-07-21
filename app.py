from db_modules.db_controller import DBController
import datetime
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
# from utils.common import generate_name

db_controller = DBController()
app = Flask(__name__)
CORS(app)
# a = db_controller.show_tables()
# db_controller.desc_table('projects')
# db_controller.print_table('projects')

@app.route('/', methods=['POST'])
def check_health():
    return jsonify({'status': 'OK'})

@app.route('/api/login', methods=['POST'])
def user_login():
    credentials = request.json
    user, email_valid, password_valid = db_controller.user_manager.get_user(credentials)
    if not email_valid:
        return jsonify({'error': 'Invalid email', 'type': 'email'})
    elif not password_valid:
        return jsonify({'error': 'Invalid password', 'type': 'password'})
    else:
        user['_id'] = str(user['user_id'])
        return jsonify(user)
    
@app.route('/api/register', methods=['POST'])
def user_register():
    user_details = request.json
    is_registered = db_controller.user_manager.create_user(user_details)
    if is_registered:
        return jsonify({'status': 'OK'})
    else:
        return jsonify({'error': 'Email already exists!'})

# Project management endpoints
@app.route('/api/get_all_projects', methods=['POST'])
def get_all_projects():
    user_id = request.json['user_id']
    projects = db_controller.project_manager.get_all_projects(user_id)
    return jsonify({'projects': projects})

@app.route('/api/create_project', methods=['POST'])
def create_project():
    project_details = request.json
    print(project_details)
    project_id = db_controller.project_manager.create_project(project_details)
    project_id = 1
    return jsonify({'project_id': str(project_id)})

@app.route('/api/delete_project', methods=['POST'])
def delete_project():
    project_id = request.json['project_id']
    db_controller.project_manager.remove_project(project_id)
    return jsonify({'project_id': project_id})

@app.route('/api/add_project_classes', methods=['POST'])
def add_project_classes():
    data = request.json
    project_id = data['project_id']
    db_controller.project_manager.push_value_by_id(project_id, data['classes_list'])
    return jsonify({'project_id': project_id})


@app.route('/api/get_training_templates', methods=['POST'])
def get_training_templates():
    data = request.json
    templates = db_controller.training_template_manager.get_table(data['data_version_id'])
  
    return jsonify(list(templates))

# Training template endpoints
@app.route('/api/create_training_template', methods=['POST'])
def create_training_template():
    template_details = request.json
    print(template_details)
    # template_id = db_controller.training_template_manager.create_version(template_details)
    # return jsonify({'template_id': str(1)})
        # str(template_id)})

# if __name__ == '__main__':
#     app.run(port=8080, debug=True, host='0.0.0.0', threaded=True)

db_controller.close()
from db_modules.db_controller import DBController
import datetime
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
# from utils.common import generate_name

db_controller = DBController()
db_controller.init_tables()
app = Flask(__name__)
CORS(app)

# db_controller.show_tables()
# db_controller.desc_table('img_items')
# db_controller.print_table('img_items')
# t = DBController().execute_query_single("SELECT COUNT(*) FROM users ")
# print(t['COUNT(*)'])
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

@app.route('/api/get_project', methods=['POST'])
def get_project():
    project_id = request.json['project_id']
    project = db_controller.project_manager.get_one_project(project_id)
    return jsonify({'project': project})

@app.route('/api/create_project', methods=['POST'])
def create_project():
    project_details = request.json
    project_id = db_controller.project_manager.create_project(project_details)
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

# Image item endpoints
@app.route('/api/get_image_items/project_version', methods=['POST'])
def get_image_items_by_project_version():
    project_id = request.json['project_id']
    images = db_controller.image_item_manager.get_image_items_by_project_version(project_id)
    return jsonify(list(images))

@app.route('/api/get_images_items/data_training_version', methods=['POST'])
def get_images_items_by_data_training_version():
    data_version_id = request.json['data_version_id']
    images = db_controller.image_item_manager.get_images_items_by_data_training_version(data_version_id)
    # print(images)
    return jsonify(list(images))


# @app.route('/api/get_training_templates', methods=['POST'])
# def get_training_templates():
#     data = request.json
#     templates = db_controller.training_template_manager.get_table(data['data_version_id'])
#     templates = []
#     return jsonify(list(templates))

# Training template endpoints
# @app.route('/api/create_training_template', methods=['POST'])
# def create_training_template():
#     template_details = request.json
#     # template_id = db_controller.training_template_manager.create_version(template_details)
#     return jsonify({'template_id': str(1)})
#         # str(template_id)})

# Annotation endpoints
@app.route('/api/get_annotations', methods=['POST'])
def get_annotations():
    project_id = request.json['project_id']
    annotations = db_controller.annotation_manager.get_annotations(project_id)
    return jsonify(list(annotations))

@app.route('/api/upload_annotations', methods=['POST'])
def upload_annotations():
    project_id = request.form['project_id']
    files = request.files.getlist('files_obj[]')
    annotation_id = db_controller.annotation_manager.create_version({"project_id": project_id})
    # total_files = db_controller.image_item_manager.upload_annotation(project_id, files, annotation_id)
    # db_controller.project_manager.set_value_by_id(project_id, {'total_images': total_files})
    # db_controller.annotation_manager.set_value_by_id(annotation_id, {'total_images': total_files})
    return jsonify({'project_id': str(project_id)})


@app.route('/api/upload_data', methods=['POST'])
def upload_data():
    files = request.files.getlist('files_obj[]')
    form_data = request.form.to_dict()
    for file in files:
        db_controller.image_item_manager.create_img_item(form_data, file)
    import random
    random_file = random.choice(files)
    db_controller.project_manager.update_avatar(form_data['project_id'], random_file)
    return jsonify({'project_id': str(form_data['project_id'])})

if __name__ == '__main__':
    app.run(port=8080, debug=True, host='0.0.0.0', threaded=True)

db_controller.close()
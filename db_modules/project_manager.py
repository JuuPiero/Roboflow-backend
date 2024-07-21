import datetime
import os
from utils.common import generate_name
import json
class ProjectManager:
    def __init__(self):
        self.table = 'projects'
        self.avatar_storage = 'storage/avatars'
        self.avatar_public_path = 'frontend/src/assets/storage/avatars'
    def create_project(self, request_form):
        from .db_controller import DBController
        DBController().execute_query("INSERT INTO projects (user_id, project_name, project_type, classes) VALUES (?,?,?,?)", (
            request_form['user_id'], request_form['project_name'], request_form['project_type'], json.dumps([]),
        ))
        new_project = dict(DBController().execute_query_single("SELECT * FROM projects ORDER BY created_at DESC LIMIT 1"))
        new_project_item_id = new_project['project_id']
        print(f'Created new project with id: {new_project_item_id}')
        return new_project_item_id

    def remove_project(self, project_id):
        from .db_controller import DBController
        DBController().execute_query("DELETE FROM projects WHERE project_id = ?", (project_id, ))
        print(f'Deleted project with id: {project_id}')

    # def set_value_by_id(self, project_id, object_value):
    #     self.project_table.update_one({'_id': ObjectId(project_id)}, {'$set': object_value})

    def push_value_by_id(self, project_id, classes):
        from .db_controller import DBController
        project = self.get_one_project(project_id)
        classes = project['classes'] + classes
        classes = json.dumps(classes)
        DBController().execute_query("UPDATE projects SET classes = ? WHERE project_id = ? ", (classes, project_id, ))

    def get_one_project(self, project_id):
        from .db_controller import DBController
        project_info = dict(DBController().execute_query_single("SELECT * FROM projects WHERE project_id = ?", (project_id, )))
        # print(project_info)
        project_info['classes'] = json.loads(project_info['classes'])
        return {**project_info,'_id': str(project_info['project_id']), 'user_id': str(project_info['user_id'])}
    
    def update_avatar(self, project_id, file_obj):
        from .db_controller import DBController
        project_info = self.get_one_project(project_id)
        if project_info['avatar_path'] and project_info['avatar_name']:
            return 
        filename = generate_name(os.path.splitext(os.path.basename(file_obj.filename))[0])
        img_paths = self._save_image(file_obj, filename)
        DBController().execute_query("UPDATE projects SET avatar_path = ? AND avatar_name = ? WHERE project_id = ? ", (img_paths['local'], filename, project_id, ))
        # self.set_value_by_id(project_id, {"avatar_path": img_paths['local']})
        # self.set_value_by_id(project_id, {"avatar_name": filename})

    def _save_image(self, file_obj, filename):
        local_path = os.path.join(self.avatar_storage, f'{filename}.jpg')
        public_path = os.path.join(self.avatar_public_path, f'{filename}.jpg')
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        os.makedirs(os.path.dirname(public_path), exist_ok=True)
        file_obj.seek(0)
        file_obj.save(local_path)
        file_obj.seek(0)
        file_obj.save(public_path)
        return {'local': local_path, 'public': public_path}
    # def show_table(self):
    #     for project in self.project_table.find():
    #         print(project)

    def get_all_projects(self, user_id):
        from .db_controller import DBController
        # print(user_id)
        projects = []
        temp = DBController().execute_query("SELECT * FROM projects WHERE user_id = ?", (int(user_id), ))
        
        for project in temp:
            project = dict(project)
            project['_id'] = str(project['project_id'])
            project['user_id'] = str(project['user_id'])
            projects.append(project)
        return projects
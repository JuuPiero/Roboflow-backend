
class AnnotationManager:
    def __init__(self):
        self.version_table = 'versions'

    def create_version(self, request_form):
        from .db_controller import DBController
        project_id = request_form['project_id']
        version_count = DBController().execute_query_single("SELECT COUNT(*) FROM versions WHERE project_id = ?", (request_form['project_id'], ))
        version_count = version_count['COUNT(*)']
        DBController().execute_query("INSERT INTO versions (project_id, version_name) VALUES (?,?)", (
            project_id, f'annotation-version-{version_count}',
        ))
        new_version = dict(DBController().execute_query_single("SELECT * FROM versions ORDER BY created_at DESC LIMIT 1"))
        new_version_id = new_version['version_id']
        print(f'Created new version with id: {new_version_id}')
        return new_version_id

    # def set_value_by_id(self, annotation_id, object_value):
    #     self.annotation_table.update_one({'_id': ObjectId(annotation_id)}, {'$set': object_value})

    def get_annotations(self, project_id):
        from .db_controller import DBController
        versions = []
        temp = DBController().execute_query("SELECT * FROM versions WHERE project_id = ?", (project_id, ))
        for version in temp:
            versions.append(dict(version))
        return [{**item, '_id': str(item['version_id'])} for item in versions]

    def show_table(self):
        for version in self.annotation_table.find():
            print(version)

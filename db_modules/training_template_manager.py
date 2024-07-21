import datetime
# from bson.objectid import ObjectId

class TrainingTemplateManager:
    def __init__(self):
        self.data_processing_table = 'data_processing'
        self.version_table = 'versions'

    def create_version(self, request_form):
        data_version_id = request_form['data_version_id']
        version_count = self.training_template_table.count_documents({'data_version_id': data_version_id})
        version_info = {
            'epoch': request_form['epoch'],
            'batch_size': request_form['batch_size'],
            'patience': request_form['patience'],
            'device': request_form['device'],
            'workers': request_form['workers'],
            'preprocess_options': request_form['preprocess_options'],
            'augmentation_options': request_form['augmentation_options'],
            'train_val_test_ratio': request_form['train_val_test_ratio'],
            'data_version_id': data_version_id,
            'training_info_id': '',
            'version_name': request_form.get('version_name', f'template-version-{version_count}'),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        new_version_id = self.training_template_table.insert_one(version_info).inserted_id
        print(f'Created new version with id: {new_version_id}')
        return new_version_id
    # def set_value_by_id(self, training_template_id, object_value):
    #     self.training_template_table.update_one({'_id': ObjectId(training_template_id)}, {'$set': object_value})

    # def push_value_by_id(self, training_template_id, object_value):
    #     self.training_template_table.update_one({'_id': ObjectId(training_template_id)}, {'$push': object_value})
    # def check_training_info_id_exist(self,training_template_id):
    #     training_template_item = self.training_template_table.find_one({'_id': ObjectId(training_template_id)})
  
    #     if training_template_item['training_info_id']:
    #         return training_template_item['training_info_id']
    #     return False
    


    # def get_table(self, data_version_id):
    #     table = self.training_template_table.find({'data_version_id': data_version_id})
    #     # for i in table:
    #     #     print(i)
    #     return [{**item, '_id': str(item['_id'])} for item in table]

    # def show_table(self):
    #     for version in self.training_template_table.find():
    #         print(version)

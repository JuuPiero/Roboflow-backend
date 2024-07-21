import datetime
# from bson.objectid import ObjectId
import os
# from utils.common import generate_name

class ImageItemManager:
    def __init__(self, image_item_table):
        self.image_item_table = image_item_table
        self.storage_path = 'storage/images'
        self.storage_public_path = 'frontend/src/assets/storage/images'

    # def create_img_item(self, request_form, file_obj):
        
    #     filename = generate_name(os.path.splitext(os.path.basename(file_obj.filename))[0])
    #     existing_item = self.image_item_table.find_one({
    #         'project_id': request_form['project_id'],
    #         'image_name': filename
    #     })
    #     if existing_item:
    #         return str(existing_item['_id'])
    #     img_paths = self._save_image(file_obj, filename)
    #     image_item_info = {
    #         'project_id': request_form['project_id'],
    #         'type': file_obj.mimetype,
    #         'image_path': img_paths['local'],
    #         'label_path': '',
    #         'image_name': filename,
    #         'annotation_id': '',
    #         'data_version_ids': [],
    #         'status': 'unassigned',
    #         'created_at': datetime.datetime.now(datetime.timezone.utc),
    #         'updated_at': datetime.datetime.now(datetime.timezone.utc)
    #     }

    #     new_image_item_id = self.image_item_table.insert_one(image_item_info).inserted_id
    #     print(f'Created new img item with id: {new_image_item_id}')
    #     return new_image_item_id

    # def _save_image(self, file_obj, filename):
    #     local_path = os.path.join(self.storage_path, f'{filename}.jpg')
    #     public_path = os.path.join(self.storage_public_path, f'{filename}.jpg')
    #     os.makedirs(os.path.dirname(local_path), exist_ok=True)
    #     os.makedirs(os.path.dirname(public_path), exist_ok=True)
    #     file_obj.seek(0)
    #     file_obj.save(local_path )
    #     file_obj.seek(0)
    #     file_obj.save(public_path)
    #     return {'local': local_path, 'public': public_path}

    # def add_label(self, image_item_id):
    #     img_item = self.get_image_item(image_item_id)
    #     if not img_item:
    #         return

    #     label_path = img_item['image_path'].replace('images', 'labels').replace('.jpg', '.txt')
    #     self.set_value_by_id(image_item_id, {'label_path': label_path, 'status': 'dataset'})
    #     print(f'Added label to img item with id: {image_item_id}')

    # def set_value_by_id(self, image_item_id, object_value):
    #     self.image_item_table.update_one({'_id': ObjectId(image_item_id)}, {'$set': object_value})

    # def push_value_by_id(self, image_item_id, object_value):
    #     self.image_item_table.update_one({'_id': ObjectId(image_item_id)}, {'$push': object_value})

    # def add_annotation_id(self, image_item_id, annotation_id):
    #     self.set_value_by_id(image_item_id, {'annotation_id': str(annotation_id)})

    # def add_data_version_id(self, image_item_id, data_version_id):
    #     self.push_value_by_id(image_item_id, {'data_version_ids': str(data_version_id)})
    #     print(f'Added version_id to img item with id: {image_item_id}')

    # def get_image_items_by_project_version(self, project_id):
    #     table = self.image_item_table.find({'project_id': project_id})
    #     return [{**item, '_id': str(item['_id'])} for item in table]

    # def get_images_items_by_data_training_version(self, data_version_id):
    #     table = self.image_item_table.find({'data_version_ids': data_version_id})
    #     return [{**item, '_id': str(item['_id'])} for item in table]
    # def get_image_item(self, image_item_id):
    #     return self.image_item_table.find_one({'_id': ObjectId(image_item_id)})

    # def upload_annotation(self, project_id, annotation_files, annotation_id):
    #     count = 0
    #     for file_obj in annotation_files:
    #         filename = generate_name(os.path.splitext(os.path.basename(file_obj.filename))[0])
    #         img_item = self.image_item_table.find_one({'project_id': project_id, 'image_name': filename})
    #         if not img_item or img_item['label_path']:
    #             continue

    #         label_path = os.path.join(self.storage_path.replace('images', 'labels'), f'{filename}.txt')
    #         os.makedirs(os.path.dirname(label_path), exist_ok=True)

    #         if os.path.exists(img_item['image_path']):
    #             print(img_item['image_path'])
    #             self.add_label(str(img_item['_id']))
    #             self.add_annotation_id(str(img_item['_id']), annotation_id)
    #             file_obj.seek(0)
    #             file_obj.save(label_path)
    #             count += 1

    #     return count

import datetime
import os
from utils.common import generate_name
import json
class ImageItemManager:
    def __init__(self):
        self.image_item_table = 'image_items'
        self.storage_path = 'storage/images'
        self.storage_public_path = 'frontend/src/assets/storage/images'

    def create_img_item(self, request_form, file_obj):
        from .db_controller import DBController
        filename = generate_name(os.path.splitext(os.path.basename(file_obj.filename))[0])
        existing_item = DBController().execute_query_single("SELECT * FROM img_items WHERE image_name = ? AND project_id = ?", (filename, request_form['project_id']))
        if existing_item:
            # existing_item = dict(existing_item)
            return str(existing_item['img_item_id'])
        img_paths = self._save_image(file_obj, filename)
        DBController().execute_query("INSERT INTO img_items (project_id, type, image_path, image_name, label_path, data_version_ids) VALUES (?,?,?,?,?,?)", (request_form['project_id'], file_obj.mimetype, img_paths['local'], filename, '', '[]', ))
        new_image_item = DBController().execute_query_single("SELECT * FROM img_items ORDER BY created_at DESC LIMIT 1")
        new_image_item_id = new_image_item['img_item_id']
        print(f'Created new img item with id: {new_image_item_id}')
        return new_image_item_id

    def _save_image(self, file_obj, filename):
        local_path = os.path.join(self.storage_path, f'{filename}.jpg')
        public_path = os.path.join(self.storage_public_path, f'{filename}.jpg')
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        os.makedirs(os.path.dirname(public_path), exist_ok=True)
        file_obj.seek(0)
        file_obj.save(local_path)
        file_obj.seek(0)
        file_obj.save(public_path)
        return {'local': local_path, 'public': public_path}

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

    def get_image_items_by_project_version(self, project_id):
        from .db_controller import DBController
        images = []
        temp = DBController().execute_query("SELECT * FROM img_items WHERE project_id = ?", (project_id, ))
        # print(temp)
        for image in temp:
            images.append(dict(image))
            
        return [{**item, '_id': str(item['img_item_id'])} for item in images]

    def get_images_items_by_data_training_version(self, data_version_ids):
        from .db_controller import DBController
        # table = self.image_item_table.find({'data_version_ids': data_version_id})
        # data_version_ids
        data_version_ids = json.dumps(data_version_ids)
        images = []
        temp = DBController().execute_query("SELECT * FROM img_items WHERE data_version_ids = ?", (data_version_ids,))
        if temp:
            for image in temp:
                images.append(dict(image))
        return [{**item, '_id': str(item['img_item_id'])} for item in images]
    
    def get_image_item(self, image_item_id):
        from .db_controller import DBController
        image = dict(DBController().execute_query_single("SELECT * FROM img_items WHERE img_item_id = ?", (image_item_id,)))
        image['_id'] = image_item_id
        return image

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

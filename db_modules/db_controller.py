from tabulate import tabulate
from .user_manager import UserManager
from .project_manager import ProjectManager
# from .image_item_manager import ImageItemManager
# from .data_training_manager import DataTrainingManager
# from .training_template_manager import TrainingTemplateManager
# from .training_info_manager import TrainingInfoManager
# from .annotation_manager import AnnotationManager
import os
import sqlite3
# //////////////////////////////////////


class DBController:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBController, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.connection = sqlite3.connect('database/ai_studio_db.db')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        # init components
        self.init_tables()
        self.init_manangers()

    def init_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                project_name TEXT NOT NULL,
                project_type TEXT NOT NULL,
                classes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS img_items (
                img_item_id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                image_name TEXT,
                image_path TEXT,
                label_path TEXT,
                data_version_ids TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS versions (
                version_id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL,
                
                FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
            )
        ''') # version_name TEXT NOT NULL,
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_processing (
                data_processing_id INTEGER PRIMARY KEY,
                version_id INTEGER NOT NULL,
                train_val_test_ratio REAL,
                preprocess_options TEXT,
                technique_options TEXT,
                FOREIGN KEY (version_id) REFERENCES versions(version_id) ON DELETE CASCADE
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_versions (
                training_version_id INTEGER PRIMARY KEY,
                version_id INTEGER NOT NULL,
                FOREIGN KEY (version_id) REFERENCES versions(version_id) ON DELETE CASCADE
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_options (
                training_version_id INTEGER NOT NULL,
                model_type TEXT,
                epochs INTEGER,
                batch_size INTEGER,
                patience INTEGER,
                device INTEGER,
                workers INTEGER,
                FOREIGN KEY (training_version_id) REFERENCES training_versions(training_version_id) ON DELETE CASCADE
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_info (
                training_version_id INTEGER NOT NULL,
                model_path TEXT,
                in_progress INTEGER,
                train_loss REAL,
                val_loss REAL,
                test_loss REAL,
                val_acc REAL,
                test_acc REAL,
                FOREIGN KEY (training_version_id) REFERENCES training_versions(training_version_id) ON DELETE CASCADE
            )
        ''')
        
        self.connection.commit()
        

    def init_manangers(self):
        self.user_manager = UserManager()
        self.project_manager = ProjectManager()
        # self.image_item_manager = ImageItemManager(self.image_item_manager)
        
        # self.data_training_manager = DataTrainingManager(self.data_training_table)
        # self.training_template_manager = TrainingTemplateManager(self.training_template_table)
        # self.annotation_manager = AnnotationManager(self.annotation_table)
        # self.training_info_manager = TrainingInfoManager(self.training_info_table)
    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            return self.cursor.fetchall()
        else:
            self.connection.commit()
            return self.cursor.rowcount

    def execute_query_single(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def commit(self):
        self.connection.commit()
        
    def show_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        return [table["name"] for table in tables]
    
    def desc_table(self, table_name):
        query = f"PRAGMA table_info({table_name});"
        self.cursor.execute(query)
        columns = self.cursor.fetchall()
        for column in columns:
            print(dict(column))
        # return columns
        
    def print_table(self, table_name):
        # Get the column names and data
        desc_query = f"PRAGMA table_info({table_name});"
        self.cursor.execute(desc_query)
        columns = self.cursor.fetchall()
        column_names = [col["name"] for col in columns]

        select_query = f"SELECT * FROM {table_name};"
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()

        # Format the data for printing
        table_data = [column_names] + [list(row) for row in rows]
        print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    
    def close(self):
        self.connection.close()
        DBController._instance = None


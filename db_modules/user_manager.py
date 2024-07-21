class UserManager:
    def __init__(self):
        self.table = 'users'

    def create_user(self, request_form):
        from .db_controller import DBController
        if not self.get_user(request_form): #check user exists
            return False
        DBController().execute_query("INSERT INTO users (first_name, last_name, email, password) VALUES (?,?,?,?)", (
            request_form['first_name'], request_form['last_name'], request_form['email'], request_form['password'],
        ))
        return True

    def get_user(self, info):
        from .db_controller import DBController
        user_item = DBController().execute_query_single("SELECT * FROM users WHERE email = ?", (info['email'], ))
        if not user_item:
            return None, False, False
        user_item = dict(user_item)
        return user_item, user_item['email'] == info['email'], user_item['password'] == info['password']

    def remove_user(self, user_id):
        from .db_controller import DBController
        DBController().execute_query("DELETE FROM user WHERE user_id = ?", (user_id, ))
        print(f'Deleted user with id: {user_id}')

    def show_table(self):
        from .db_controller import DBController
        users =  DBController().execute_query("SELECT * FROM users")
        for user in users:
            print(dict(user))

    def get_table(self):
        from .db_controller import DBController
        list_users = []
        users = DBController().execute_query("SELECT * FROM users")
        for user in users:
            list_users.append(dict(user))
        return list_users

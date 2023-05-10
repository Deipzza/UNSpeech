from flask_login import LoginManager, UserMixin

from .database.mongodatabase import *
from .login import *

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, username,  data, password = None):
        self.username = username
        self.password = password
        self.data = data
    
    def is_active(self):
        return True
    
    def is_authenticated(self):
        if self.data["user"]["uid"] == self.username:
            return True
        return False
    
    def get_id(self):
        return str(self.username)

from pymongo import MongoClient, DESCENDING
from bcrypt import hashpw, checkpw, gensalt
import yaml

class Users:
    """ A class to store and retrieve user info and passwords to MongoDB.

    """
    def __init__(self):
        f = open("config.cfg", 'r')
        settings = yaml.load(f)
        self.mongo_client = MongoClient(settings['mongo_ip'], settings['mongo_port'])
        self.mongo_db = self.mongo_client['userinfo']
        self.userinfo = self.mongo_db['userinfo']

        f.close()

    def get_user_info(self, username, password):
        user = self.userinfo.find_one({'username':username})
        if user is not None:
            # Check password with given password
            if checkpw(password.encode('utf-8'), user['password']):
                # If correct, return user_id
                return user['user_id']
            else:
                # Else return False
                return False
        else:
            # Return error
            return None

    def create_user(self, username, password):
        if self.userinfo.find({'username':username}).count() > 0:
            return False
        else:
            # Create user
            # Find user with highest user_id and increment
            highest_user_id = self.userinfo.find_one(sort=[("user_id",DESCENDING)])
            if highest_user_id is None:
                user_id = 1
            else:
                user_id = highest_user_id["user_id"] + 1
            # Hash password
            hashed = hashpw(password.encode('utf-8'), gensalt())
            # Set user
            self.userinfo.insert_one({"username":username,"password":hashed,"user_id":user_id})
            return user_id

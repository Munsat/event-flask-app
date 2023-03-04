from database import sql_select_all, sql_write, sql_select_one
from werkzeug.security import check_password_hash

class User:
    def __init__(self,id,name, email, hashed_password) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password

    def validate_password(self, password):
            return check_password_hash(self.hashed_password,password)
                 

def insert_user(name, email, hashed_password):
    return sql_write('INSERT INTO users (name,email,hashed_password) VALUES (%s, %s, %s)',[name, email, hashed_password])

def select_user_by_email(email):
     user =  sql_select_one('SELECT id,name,email,hashed_password FROM users WHERE email=%s',[email])
     return User(user['id'],user['name'], user['email'], user['hashed_password'])
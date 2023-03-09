from database import sql_select_all, sql_write, sql_select_one,sql_write_with_return, sql_delete
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
    id =  sql_write_with_return('INSERT INTO users (name,email,hashed_password) VALUES (%s, %s, %s) RETURNING id',[name, email, hashed_password])
    return id

def select_user_by_email(email):
     user =  sql_select_one('SELECT id,name,email,hashed_password FROM users WHERE email=%s',[email])
     return User(user['id'],user['name'], user['email'], user['hashed_password']) if user != None else None

def get_all_user_emails():
    return sql_select_all('SELECT email FROM users')

def delete_user(id):
     return sql_delete("DELETE FROM users WHERE id=%s",[id])

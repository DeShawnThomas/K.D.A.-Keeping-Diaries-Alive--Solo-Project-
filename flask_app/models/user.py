from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import check_password_hash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:

    db="kda_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.riot_identification=data['riot_identification']
        self.favorite_agent=data['favorite_agent']
        self.current_rank=data['current_rank']
        self.goal_rank=data['goal_rank']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    #Create
    @classmethod
    def save(cls,data):
        query="INSERT INTO users(first_name,last_name,email,password,riot_identification,favorite_agent,current_rank,goal_rank) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(riot_identification)s,%(favorite_agent)s,%(current_rank)s,%(goal_rank)s)"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    #Get All
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    #Get One By Email
    @classmethod
    def get_one_by_email(cls, email):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(cls.db).query_db(query, {'email': email})
        if not results:
            return False
        return cls(results[0])

    #Get One
    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id': id}
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    #Update
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, riot_identification = %(riot_identification)s, favorite_agent = %(favorite_agent)s, current_rank = %(current_rank)s, goal_rank = %(goal_rank)s, updated_at = %(updated_at)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    #Delete
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM users WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        return results

    #User validation with flash messages grouped by register    
    @staticmethod
    def validate_user(user):
        is_valid=True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "register")
            is_valid = False
        if len(user['email']) < 1:
            flash("Email must be entered.", "register")
            is_valid = False
        elif User.get_one_by_email(user['email']):
            flash("Email is already taken", "register")
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Password and confirmation password do not match.", "register")
            is_valid = False
        if len(user['riot_identification']) > 16:
            flash("Riot identification is too long.", "register")
            is_valid = False
        if '#' not in user['riot_identification']:
            flash("Riot identification must include a '#' character", "register")
            is_valid = False
        if user['favorite_agent'] == '':
            flash("Must enter favorite agent. The creator of this app really likes Killjoy :D", "register")
        if user['current_rank'] == '':
            flash("Must enter your current rank. There is even an option for 'unranked' before you protest!", "register")
        if user['goal_rank'] == '':
            flash("Must enter a goal rank. The creator of this app is hardstuck Diamond but he's got Ascendant dreams!", "register")
        return is_valid
    
    #User validation with flash messages grouped by login  
    @staticmethod
    def validate_login(user):
        is_valid = True
        if not user['email']:
            flash("Email must be entered.", "login")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "login")
            is_valid = False
        if not user['password']:
            flash("Password must be entered.", "login")
            is_valid = False
        elif len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "login")
            is_valid = False
        return is_valid

    #check password hashing  
    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)
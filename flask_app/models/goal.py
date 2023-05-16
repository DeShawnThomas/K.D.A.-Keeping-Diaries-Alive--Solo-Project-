from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Goal:
    db="kda_schema"

    def __init__(self, data):
        self.id = data['id']
        self.goal_date = data['goal_date']
        self.daily_goal = data['daily_goal']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    #Combining all the goals to the users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM goals JOIN users on goals.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        goals = []
        for row in results:
            new_goal = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "riot_identification": row['riot_identification'],
                "favorite_agent": row['favorite_agent'],
                "current_rank": row['current_rank'],
                "goal_rank": row['goal_rank'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            new_goal.creator = user.User(user_data)
            goals.append(new_goal)
        return goals
    
    #Need this to get a specific gaol from user
    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM goals JOIN users on goals.user_id = users.id WHERE goals.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        one_goal = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "riot_identification": result['riot_identification'],
                "favorite_agent": result['favorite_agent'],
                "current_rank": result['current_rank'],
                "goal_rank": result['goal_rank'],
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        one_goal.creator = user.User(user_data)
        return one_goal
    
    @classmethod
    def get_all_by_user(cls, user_id):
        query = f"SELECT * FROM goals WHERE user_id = {user_id}"
        results = connectToMySQL(cls.db).query_db(query)
        goals = []
        for result in results:
            goals.append(cls(result))
        return goals

    #Save
    @classmethod
    def save(cls, data):
        query = "INSERT INTO goals (goal_date, daily_goal, user_id) VALUES (%(goal_date)s, %(daily_goal)s, %(user_id)s);"
        print("Save query:", query)  # Add this line to check the query
        print("Save data:", data)    # Add this line to check the data
        return connectToMySQL(cls.db).query_db(query, data)

    #Update
    @classmethod
    def update(cls,data):
        query = "UPDATE goals SET goal_date = %(goal_date)s, daily_goal = %(daily_goal)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    #Delete
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM goals WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    #These are how we validate the goals going in the database
    @staticmethod
    def validate_goal(data):
        is_valid = True

        if data['goal_date'] == "":
            flash("A date is needed!", "diary")
            is_valid = False

        if data['daily_goal'] == "":
            flash("Please enter at least one goal in the form of a sentence.", "diary")
            is_valid = False
            
        return is_valid

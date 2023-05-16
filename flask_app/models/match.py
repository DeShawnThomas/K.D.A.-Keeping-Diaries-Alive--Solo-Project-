from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
import re


class Match:
    db = "kda_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.match_date = data["match_date"]
        self.start_rank = data["start_rank"]
        self.agent = data["agent"]
        self.map = data["map"]
        self.team_mvp = data["team_mvp"]
        self.match_mvp = data["match_mvp"]
        self.win_loss = data["win_loss"]
        self.my_score = data["my_score"]
        self.opp_score = data["opp_score"]
        self.kills = data["kills"]
        self.deaths = data["deaths"]
        self.assists = data["assists"]
        self.headshot_percentage = data["headshot_percentage"]
        self.adr = data["adr"]
        self.acs = data["acs"]
        self.diary_entry = data["diary_entry"]
        self.youtube_link = data["youtube_link"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.creator = None

    # Combining all the matches to the users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM matches JOIN users on matches.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        matches = []
        for row in results:
            valorant_match = cls(row)
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "",
                "riot_identification": row["riot_identification"],
                "favorite_agent": row["favorite_agent"],
                "current_rank": row["current_rank"],
                "goal_rank": row["goal_rank"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            valorant_match.creator = user.User(user_data)
            matches.append(valorant_match)
        return matches

    # Need this to get a specific match from user
    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM matches JOIN users on matches.user_id = users.id WHERE matches.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return False

        result = result[0]
        one_match = cls(result)
        user_data = {
            "id": result["users.id"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "email": result["email"],
            "password": "",
            "riot_identification": result["riot_identification"],
            "favorite_agent": result["favorite_agent"],
            "current_rank": result["current_rank"],
            "goal_rank": result["goal_rank"],
            "created_at": result["users.created_at"],
            "updated_at": result["users.updated_at"],
        }
        one_match.creator = user.User(user_data)
        return one_match

    # old method was not working, testing this way... jk broke it but now we have the way to get all the matches from a user
    @classmethod
    def get_all_by_user(cls, user_id):
        query = f"SELECT * FROM matches WHERE user_id = {user_id}"
        results = connectToMySQL(cls.db).query_db(query)
        matches = []
        for result in results:
            matches.append(cls(result))
        return matches

    # Save
    @classmethod
    def save(cls, data):
        query = "INSERT INTO matches (match_date,start_rank,agent,map,team_mvp,match_mvp,win_loss,my_score,opp_score,kills,deaths,assists,headshot_percentage,adr,acs,diary_entry,youtube_link,user_id) VALUES (%(match_date)s,%(start_rank)s,%(agent)s,%(map)s,%(team_mvp)s,%(match_mvp)s,%(win_loss)s,%(my_score)s,%(opp_score)s,%(kills)s,%(deaths)s,%(assists)s,%(headshot_percentage)s,%(adr)s,%(acs)s,%(diary_entry)s,%(youtube_link)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    # Update
    @classmethod
    def update(cls, data):
        query = "UPDATE matches SET match_date = %(match_date)s, start_rank =%(start_rank)s, agent = %(agent)s ,map = %(map)s,  team_mvp = %(team_mvp)s, match_mvp = %(match_mvp)s, win_loss = %(win_loss)s, my_score %(my_score)s, opp_score = %(opp_score)s, kills = %(kills)s, deaths = %(deaths)s, assists = %(assists)s, headshot_percentage = %(headshot_percentage)s, adr = %(adr)s, acs = %(acs)s, diary_entry = %(diary_entry)s, youtube_link = %(youtube_link)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    # Delete
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM matches WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_match(data):
        is_valid = True

        if data["match_date"] == "":
            flash("A match date is needed. I know you'd like to forget this one... but we need it to log the info!", "entry")
            is_valid = False

        if data["start_rank"] == "":
            flash("I know you're embarrassed about being hardstuck, but you need to enter the rank you started this match with.", "entry")
            is_valid = False

        if data["agent"] == "":
            flash("An agent must be selected. Would be very hard to play a match with no agent.", "entry")
            is_valid = False

        if data["map"] == "":
            flash("A map must be selected. Unless you played a match in the training range somehow?", "entry")
            is_valid = False

        if "team_mvp" not in data or data["team_mvp"] == "":
            flash("You need to select whether you were the team MVP or not.", "entry")
            is_valid = False

        if "match_mvp" not in data or data["match_mvp"] == "":
            flash("You must enter if you match MVP'd. I know you might have missed this one through the tears of match mvp'ing and losing... but we need to log this information.", "entry")
            is_valid = False

        if "win_loss" not in data or data["win_loss"] == "":
            flash("Did you win or lose the game? Or worse... did you tie?", "entry")
            is_valid = False

        if data["my_score"] == "":
            flash("What was your team's score this game?", "entry")
            is_valid = False

        if data["opp_score"] == "":
            flash("What was the enemy team's score this game?", "entry")
            is_valid = False

        if not data["kills"].isdigit():
            flash("Kills should be a numeric value.", "entry")
            is_valid = False

        if not data["deaths"].isdigit():
            flash("Deaths should be a numeric value.", "entry")
            is_valid = False

        if not data["assists"].isdigit():
            flash("Assists should be a numeric value.", "entry")
            is_valid = False

        if not data["headshot_percentage"].isdigit():
            flash("HS percent should be a numeric value. No need to add a '%'", "entry")
            is_valid = False

        if not data["adr"].isdigit():
            flash("Average Damage per Round should be a numeric value.", "entry")
            is_valid = False

        if not data["acs"].isdigit():
            flash("Average Combat Score should be a numeric value.", "entry")
            is_valid = False

        if data["diary_entry"] == "":
            flash("Look, I know you don't wanna talk about that VCT locked in Jett/Reyna smurf who destroyed you, but let's talk about it.", "entry")
            is_valid = False

        youtube_link = data["youtube_link"]
        if youtube_link != "" and not re.match(r"^https?://(www\.)?youtube\.com/watch\?v=[\w-]+$", youtube_link):
            flash("YouTube link is not valid. Please use a link in the format https://www.youtube.com/watch?v=VIDEO_ID", "entry")
            is_valid = False

        return is_valid

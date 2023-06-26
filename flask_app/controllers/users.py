from flask import render_template, request, session, redirect, flash
from flask_app import app
from flask_app import agent_images, rank_icons, map_loads
from flask_app.models.user import User
from flask_app.models.match import Match
from flask_app.models.goal import Goal
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/register')
def register():
    # Render the register.html template
    return render_template('register.html')

@app.route('/login')
def login():
    # Render the login.html template
    return render_template('login.html')

@app.route('/create', methods=['POST'])
def create_user():
    # Validate user registration form
    if not User.validate_user(request.form):
        return redirect('/register')
    
    user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": request.form['password'],
        "confirm_password": request.form['confirm_password'],
        "riot_identification": request.form['riot_identification'],
        "favorite_agent": request.form['favorite_agent'],
        "current_rank": request.form['current_rank'],
        "goal_rank": request.form['goal_rank'],
    }

    # Hash the password before storing it in the database
    hashed_password = bcrypt.generate_password_hash(user_data['password'])
    user_data['password'] = hashed_password
    
    # Save the user in the database and retrieve the user ID
    user_id = User.save(user_data)
    
    # Store the user ID in the session
    session['user_id'] = user_id
    
    return redirect('/dashboard')

@app.route('/returning', methods=['POST'])
def login_user():
    # Retrieve user information by email
    user = User.get_one_by_email(request.form['email'])

    # Validate login form
    if not User.validate_login(request.form):
        return redirect('/login') 

    if not user:
        flash("Invalid Email","login")
        return redirect('/login')

    # Check if the password matches the hashed password in the database
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/login')

    # Store the user ID in the session
    session['user_id'] = user.id

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    
    user_id = session['user_id']
    user = User.get_one(user_id)
    matches = Match.get_all_by_user(user_id)
    goals = Goal.get_all_by_user(user_id)
    reversed_goals = list(reversed(goals))

    # Render the dashboard.html template and pass the necessary data
    return render_template('dashboard.html', user=user, rank_icons=rank_icons, agent_images=agent_images, matches=matches, map_loads=map_loads, daily_goals=reversed_goals)

@app.route('/edit')
def edit():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    
    user_id = session['user_id']
    user = User.get_one(user_id)

    if not user:
        return redirect('/logout')

    # Render the edit_profile.html template and pass the user information
    return render_template('edit_profile.html', user=user)

@app.route('/edit/profile/', methods=['POST'])
def edit_profile():
    # Validate user update form
    if not User.validate_user_update(request.form):
        return redirect('/edit')
    
    user_id = session['user_id']
    
    user_data = {
        "id": user_id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": request.form['password'],
        "confirm_password": request.form['confirm_password'],
        "riot_identification": request.form['riot_identification'],
        "favorite_agent": request.form['favorite_agent'],
        "current_rank": request.form['current_rank'],
        "goal_rank": request.form['goal_rank'],
    }

    # Hash the password before updating it in the database
    hashed_password = bcrypt.generate_password_hash(user_data['password'])
    user_data['password'] = hashed_password

    # Update the user in the database
    User.update(user_data)

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('user_id', None)
    session.clear()
    return redirect('/')

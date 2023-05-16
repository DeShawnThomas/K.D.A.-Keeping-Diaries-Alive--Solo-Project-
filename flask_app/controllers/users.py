from flask import render_template,request,session,redirect,flash
from flask_app import app
from flask_app import agent_images, rank_icons
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/create', methods=['POST'])
def create_user():
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

    hashed_password = bcrypt.generate_password_hash(user_data['password'])
    user_data['password'] = hashed_password
    
    user_id = User.save(user_data)
    
    session['user_id'] = user_id
    
    return redirect('/dashboard')

@app.route('/returning', methods=['POST'])
def login_user():
    user = User.get_one_by_email(request.form['email'])

    if not User.validate_login(request.form):
        return redirect('/login') 

    if not user:
        flash("Invalid Email","login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/login')

    session['user_id'] = user.id

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_one(session['user_id'])

    return render_template('dashboard.html', user=user, rank_icons=rank_icons)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

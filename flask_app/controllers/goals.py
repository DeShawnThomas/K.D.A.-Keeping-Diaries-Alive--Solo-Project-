from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.goal import Goal

@app.route('/dailygoals')
def daily_goal():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_one(session['user_id'])

    return render_template('daily_goal.html', user=user)

@app.route('/dailygoals/entry', methods=['POST'])
def save_goal():
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Goal.validate_goal(request.form):
        return redirect('/dailygoals')

    data = {
        'user_id': session['user_id'],
        'goal_date': request.form['goal_date'],
        'daily_goal': request.form['daily_goal'],
    }

    Goal.save(data)
    return redirect('/dashboard')
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.goal import Goal

@app.route('/dailygoals')
def daily_goal():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')

    # Retrieve user information from the session
    user = User.get_one(session['user_id'])

    # Render the daily_goal.html template and pass the user information
    return render_template('daily_goal.html', user=user)

@app.route('/dailygoals/entry', methods=['POST'])
def save_goal():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')

    # Validate the submitted goal
    if not Goal.validate_goal(request.form):
        return redirect('/dailygoals')

    # Prepare the data to save the goal
    data = {
        'user_id': session['user_id'],
        'goal_date': request.form['goal_date'],
        'daily_goal': request.form['daily_goal'],
    }

    # Save the goal
    Goal.save(data)

    # Redirect to the dashboard page after saving the goal
    return redirect('/dashboard')

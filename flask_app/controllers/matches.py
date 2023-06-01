from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.match import Match
from flask_app.models.user import User
from flask_app import agent_images, rank_icons, map_loads

@app.route('/new/diary')
def new_diary():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_one(session['user_id'])

    return render_template('new_diary.html', user=user, agent_images=agent_images, rank_icons=rank_icons, map_loads=map_loads)


@app.route('/new/diary/entry', methods=['POST'])
def diary_entry():
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Match.validate_match(request.form):
        return redirect('/new/diary')

    data = {
        'user_id': session['user_id'],
        'match_date': request.form['match_date'],
        'start_rank': request.form['start_rank'],
        'agent': request.form['agent'],
        'map': request.form['map'],
        'team_mvp': request.form['team_mvp'],
        'match_mvp': request.form['match_mvp'],
        'win_loss': request.form['win_loss'],
        'my_score': request.form['my_score'],
        'opp_score': request.form['opp_score'],
        'kills': request.form['kills'],
        'deaths': request.form['deaths'],
        'assists': request.form['assists'],
        'headshot_percentage': request.form['headshot_percentage'],
        'adr': request.form['adr'],
        'acs': request.form['acs'],
        'diary_entry': request.form['diary_entry'],
        'youtube_link': request.form['youtube_link'],
    }

    Match.save(data)
    return redirect('/dashboard')

@app.route('/matchstats')
def all_matches():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_one(session['user_id'])

    matches = Match.get_all_by_user(session['user_id'])
    sorted_matches = sorted(matches, key=lambda match: match.match_date)

    return render_template('all_matches.html', user=user, matches=sorted_matches, agent_images=agent_images, rank_icons=rank_icons, map_loads=map_loads)

@app.route('/diaryentries')
def all_entries():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_one(session['user_id'])

    matches = Match.get_all_by_user(session['user_id'])
    sorted_matches = sorted(matches, key=lambda match: match.match_date)

    return render_template('all_diary.html', user=user, matches=sorted_matches, agent_images=agent_images, rank_icons=rank_icons, map_loads=map_loads)

@app.route('/match/<int:id>')
def view_match(id):
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_one(session['user_id'])

    return render_template('view_match.html', user=user, match=Match.get_one_by_id({'id': id, 'user_id': session['user_id']}))

@app.route('/edit/<int:id>')
def edit_match(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_one(session['user_id'])

    return render_template('edit_match.html', user=user,match=Match.get_one_by_id({'id': id, 'user_id': session['user_id']}))

@app.route('/edit/stats/<int:id>', methods=['POST'])
def edit_match_played(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Match.validate_match(request.form):
        return redirect(f'/edit/{id}')

    data = {
        'id': id,
        'user_id': session['user_id'],
        'match_date': request.form['match_date'],
        'start_rank': request.form['start_rank'],
        'agent': request.form['agent'],
        'map': request.form['map'],
        'team_mvp': request.form['team_mvp'],
        'match_mvp': request.form['match_mvp'],
        'win_loss': request.form['win_loss'],
        'my_score': request.form['my_score'],
        'opp_score': request.form['opp_score'],
        'kills': request.form['kills'],
        'deaths': request.form['deaths'],
        'assists': request.form['assists'],
        'headshot_percentage': request.form['headshot_percentage'],
        'adr': request.form['adr'],
        'acs': request.form['acs'],
        'diary_entry': request.form['diary_entry'],
        'youtube_link': request.form['youtube_link'],
    }
    
    Match.update(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def never_happened(id):
    if 'user_id' not in session:
        return redirect('/logout')

    Match.delete({'id':id, 'user_id': session['user_id']})
    return redirect('/dashboard')

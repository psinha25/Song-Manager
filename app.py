from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__) # referencing this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class ListenMusic(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    song = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # return a string everytime we create a new element
    def __repr__(self):
        return '<Song %r>' % self.id

class HatedMusic(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    hated_song = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # return a string everytime we create a new element
    def __repr__(self):
        return '<Hated Song %r>' % self.id

class LovedMusic(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    loved_song = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # return a string everytime we create a new element
    def __repr__(self):
        return '<Loved Song %r>' % self.id

# url string of your route
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST' and 'listen_to_button' in request.form:
        song_content = request.form['content']
        new_song = ListenMusic(song = song_content)
        try:
            db.session.add(new_song)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding a new song to your list'
    elif request.method == 'POST' and 'hate_button' in request.form:
        song_content = request.form['content']
        new_song = HatedMusic(hated_song = song_content)
        try:
            db.session.add(new_song)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding a new song to your list'
    elif request.method == 'POST' and 'love_button' in request.form:
        song_content = request.form['content']
        new_song = LovedMusic(loved_song = song_content)
        try:
            db.session.add(new_song)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding a new song to your list'
    else: 
        listen_songs = ListenMusic.query.order_by(ListenMusic.date_created).all()
        hated_songs = HatedMusic.query.order_by(HatedMusic.date_created).all()
        loved_songs = LovedMusic.query.order_by(LovedMusic.date_created).all()
        return render_template('index.html', listen_songs = listen_songs, hated_songs = hated_songs, loved_songs = loved_songs)

@app.route('/delete_listen_to/<int:id>')
def delete_listen_to(id):
    song_to_delete = ListenMusic.query.get_or_404(id)
    try:
        db.session.delete(song_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the specified song from your list'

@app.route('/delete_hated/<int:id>')
def delete_hated(id):
    song_to_delete = HatedMusic.query.get_or_404(id)
    try:
        db.session.delete(song_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the specified song from your list'

@app.route('/delete_loved/<int:id>')
def delete_loved(id):
    song_to_delete = LovedMusic.query.get_or_404(id)
    try:
        db.session.delete(song_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the specified song from your list'

@app.route('/update_listen_to/<int:id>', methods = ['GET', 'POST'])
def update_listen_to(id):
    song_to_update = ListenMusic.query.get_or_404(id)
    if request.method == 'POST':
        song_to_update.song = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update_listen_to.html', listen_to_song = song_to_update)

@app.route('/update_hated/<int:id>', methods = ['GET', 'POST'])
def update_hated(id):
    song_to_update = HatedMusic.query.get_or_404(id)
    if request.method == 'POST':
        song_to_update.hated_song = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update_hated.html', hated_song = song_to_update)

@app.route('/update_loved/<int:id>', methods = ['GET', 'POST'])
def update_loved(id):
    song_to_update = LovedMusic.query.get_or_404(id)
    if request.method == 'POST':
        song_to_update.loved_song = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update_loved.html', loved_song = song_to_update)

if __name__ == '__main__':
    app.run(debug = True) 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///game.db'
db = SQLAlchemy(app)

# 定义玩家模型
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    scores = db.relationship('Score', backref='player', lazy=True)

# 定义分数模型
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_score', methods=['POST'])
def submit_score():
    name = request.form['name']
    score = int(request.form['score'])

    player = Player.query.filter_by(name=name).first()
    if player:
        new_score = Score(score=score, player=player)
        db.session.add(new_score)
    else:
        new_player = Player(name=name)
        db.session.add(new_player)
        db.session.flush()
        new_score = Score(score=score, player=new_player)
        db.session.add(new_score)

    db.session.commit()
    return redirect(url_for('score_history'))

@app.route('/score_history')
def score_history():
    players = Player.query.all()
    return render_template('score_history.html', players=players)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
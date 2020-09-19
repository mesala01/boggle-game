from flask import Flask, request, render_template, jsonify, session, url_for, redirect
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "qsdesafgthklponmb"

boggle_game = Boggle()


@app.route("/")
def homepage():
    """Show board."""

    board = boggle_game.make_board()
    session['board'] = board
    highestscore = session.get("highestscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("index.html", board=board,
                           highestscore=highestscore,
                           nplays=nplays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highestscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highestscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)



@app.route("/reset")
def reset_game():
    """ reset the game values """
    session['nplays'] = 0
    session['highestscore'] = 0
    return redirect(url_for('homepage'))


@app.route("/newgame")
def new_game():
    """ quit and get new game"""
    return redirect(url_for('homepage'))


from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from guess.auth import login_required
from guess.db import get_db
from random import randint

bp = Blueprint('play', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    # Get list of users current games
    games = db.execute(
        "SELECT id, guesses FROM game"
        " WHERE user_id = ?",
        (g.user['id'],)
    ).fetchall()

    return render_template('play/index.html', games=games)


@bp.route('/new')
@login_required
def new_game():
    db = get_db()
    # Generate random number
    number = randint(1, 100)
    # Create game in database
    db.execute(
        "INSERT INTO game (number, guesses, user_id) VALUES (?, 0, ?)",
        (number, g.user['id'])
    )
    db.commit()

    return redirect(url_for('index'))


@bp.route('/play/<int:game_id>', methods=('GET', 'POST'))
def play_game(game_id):
    """ Show the current game info and/or process a guess """
    db = get_db()
    msg = None

    if request.method == 'POST':
        db.execute(
            "UPDATE game"
            " SET guesses = guesses + 1"
            " WHERE game.id = ?",
            (game_id,)
        )
        db.commit()
        guess = request.form.get('guess', type=int)
        game = db.execute(
            "SELECT guesses, number FROM game WHERE id = ?",
            (game_id,)
        ).fetchone()
        if guess > game['number']:
            msg = "Too high"
        elif guess < game['number']:
            msg = "Too low"
        else:
            db.execute("DELETE FROM game WHERE id = ?", (game_id,))
            db.commit()
            return render_template('play/win.html', game=game)

    game = db.execute(
        "SELECT game.id, guesses, user_id, username"
        " FROM game JOIN user ON game.user_id = user.id"
        " WHERE game.id = ?",
        (game_id,)
    ).fetchone()

    if msg is not None:
        flash(msg)

    return render_template('play/game.html', game=game)

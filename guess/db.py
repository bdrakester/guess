import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables. """
    init_db()
    click.echo('Initialized database.')


@click.command('show-db-user')
@with_appcontext
def show_db_user_command():
    """ Print the user table. """
    db = get_db()
    users = db.execute('SELECT * FROM user').fetchall()
    click.echo('user table:')
    for row in users:
        for column in row:
            click.echo(column, nl=False)
            click.echo(' | ', nl=False)
        click.echo()


@click.command('add-user')
@click.argument('username')
@click.argument('password')
@with_appcontext
def add_user_command(username, password):
    db = get_db()
    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()

@click.command('show-db-game')
@with_appcontext
def show_db_game_command():
    """ Print the game table """
    db = get_db()
    games = db.execute('SELECT * FROM game').fetchall()
    click.echo('game table:')
    for row in games:
        for column in row:
            click.echo(column, nl=False)
            click.echo(' | ', nl=False)
        click.echo()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(show_db_user_command)
    app.cli.add_command(add_user_command)
    app.cli.add_command(show_db_game_command)
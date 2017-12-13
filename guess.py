###############################################################################
# 12/12/2017 - Brian Drake
#
# Guess! Web application.
#
# A simple number guessing game.  Written to learn Python web programming.
# Uses the Bottle framework
#
###############################################################################

from bottle import Bottle, template, static_file, request
import sqlite3

guessApp = Bottle()


@guessApp.route('/')
def index():
    """ The Home Page """

    #messages = dict()
    #messsages['output'] = ''

    return template('index.tpl') 

@guessApp.post('/')
def post_index():
    """ Submit a guess """

    guess = request.forms.get('guess', type=int)
    messages = dict()
    messages['output'] = 'You guessed ' + str(guess)
    
    return template('index.tpl', messages)


@guessApp.route('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root='static')


if __name__ == "__main__":
    guessApp.run(debug=True)

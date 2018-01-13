###############################################################################
# 12/12/2017 - Brian Drake
#
# Guess! Web application.
#
# A simple number guessing game.  Written to learn Python web programming.
# Uses the Bottle framework
#
###############################################################################

from bottle import Bottle, template, static_file, request, response, redirect
import sqlite3, uuid, random

class dbguessapp:
    """
    Provide an interface to the database
    """

    def __init__(self):
        """
        Construct a database connection. Uses a sqlite3 database file
        named dbguessapp.db
        """
        self.dbname = "dbguessapp.db"

        self.conn = sqlite3.connect(self.dbname)

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()
        
    def create_tables(self):
        """
        Create database tables for the Guess application.
        """
        cursor = self.cursor()
        cursor.execute("DROP TABLE IF EXISTS sessions")
        cursor.execute("DROP TABLE IF EXISTS numbers")
        cursor.execute("""
        CREATE TABLE sessions (
            key text primary key
        )
        """)
        cursor.execute("""
        CREATE TABLE numbers (
            key text,
            number int,
            guesses int
        )
        """)
  
    def new_session(self):
        """
        Add new session to sessions table, generate random number and
        add to numbers table.  Return the session key.
        """
        cursor = self.cursor()

        # Use the uuid library to generate session key
        key = str(uuid.uuid4())
        
        # Use the random libary to generate a random integer
        randomNumber = random.randint(1,100)

        # Import the session key and random integer into numbers table
        cursor = self.cursor()
        cursor.execute("INSERT INTO sessions VALUES (?)", (key,))
        cursor.execute("INSERT INTO numbers VALUES (?, ?, 0)",
                       (key, randomNumber))
        self.commit()

        return key
    def session_exists(self, key):
        """
        Return True if a session for key exists in the database, else return
        false.
        """
        cursor = self.cursor()
        cursor.execute("SELECT COUNT (key) FROM sessions WHERE key = ?", (key,))
        if cursor.fetchone()[0] == 1:
            #print("COUNT == 1")
            return True
        else:
            #print("ELSE ...")
            return False
        
    def get_number(self, key):
        """
        Return the random number associated with session key
        """
        cursor = self.cursor()
        cursor.execute("SELECT number FROM numbers WHERE key = ?", (key,))

        return cursor.fetchone()[0]
        
    def delete_session(self, key):
        """
        Delete the session from sessions and numbers tables.
        """
        cursor = self.cursor()
        cursor.execute("DELETE FROM numbers WHERE key = ?", (key,))
        cursor.execute("DELETE FROM sessions WHERE key = ?", (key,))

    def get_guesses(self, key):
        """
        Return the number of geusses for the session key
        """
        cursor = self.cursor()
        cursor.execute("SELECT guesses FROM numbers WHERE key = ?", (key,))

        return cursor.fetchone()[0]

    def set_guesses(self, key, guesses):
        """
        Set the number of guesses for session key
        """
        cursor = self.cursor()
        cursor.execute("""
        UPDATE Numbers
        SET guesses = ?
        WHERE key = ? 
        """, (guesses, key))

        self.commit()
        
        
    def increment_guesses(self, key):
        """
        Increment guesses by 1
        """
        cursor = self.cursor()
        guesses = self.get_guesses(key)
        self.set_guesses(key, guesses + 1)
        

guessApp = Bottle()
COOKIE_NAME = 'guessSession'

@guessApp.route('/')
def index():
    """ The Home Page """

    key = request.get_cookie(COOKIE_NAME)
    
    # If no session cookie, create session, set cookie
    if key == None:
        key = guessAppDB.new_session()
        response.set_cookie(COOKIE_NAME, key)

    # If session cookie exists, but there is no session
    elif not guessAppDB.session_exists(key):
        key = guessAppDB.new_session()
        response.set_cookie(COOKIE_NAME, key)
        
    messages = dict()
    messages['output'] = ''

    return template('index.tpl', messages) 

@guessApp.post('/')
def post_index():
    """ Submit a guess """

    key = request.get_cookie(COOKIE_NAME)

    # If there is no session for key, create new session
    if not guessAppDB.session_exists(key):
        key = guessAppDB.new_session()
        response.set_cookie(COOKIE_NAME, key)
    
    randomNum = guessAppDB.get_number(key)
    
    guess = request.forms.get('guess', type=int)
    guessAppDB.increment_guesses(key)
    
    ##### BEGIN DEBUG ######
    #guesses = guessAppDB.get_guesses(key)
    ##### END DEBUG   ######

    messages = dict()

    # If they guessed right
    if guess == randomNum:
        #messages['output'] = 'Congrats!! ' + str(guess) + ' is the number!'
        return redirect('/win')

    # If the guess larger 
    elif guess > randomNum:
        messages['output'] = str(guess) + ' is too high...'

    # Else the guest is smaller
    else:
        messages['output'] = str(guess) + ' is too low...'

    ##### BEGIN DEBUG ######
    #messages['output'] = messages['output'] + ' guesses = ' + str(guesses)
    #messages['output'] = messages['output'] + ' ..randNum = ' + str(randomNum)
    ##### END DEBUG   ######

    return template('index.tpl', messages)

@guessApp.post('/newgame')
def post_newgame():
    """ Start a new game. Delete session from database. """

    key = request.get_cookie(COOKIE_NAME)
    guessAppDB.delete_session(key)
    response.delete_cookie(COOKIE_NAME)
    
    return redirect('/')    

@guessApp.route('/win')
def win():
    """ Winner page """
    messages = dict()
    key = request.get_cookie(COOKIE_NAME)
    randomNum = guessAppDB.get_number(key)
    guesses = guessAppDB.get_guesses(key)
    
    messages['number'] = randomNum
    messages['guesses'] = guesses
    
    return template('congrats.tpl', messages)

@guessApp.route('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root='static')


if __name__ == "__main__":
    guessAppDB = dbguessapp()
    guessAppDB.create_tables()
    guessApp.run(debug=True)

from Flask import flask,g
import sqlite

app = Flask(__name__)


def db_connection():
    sql= sqlite.connect('./my_database#.db')
    sql.row_factory= sqlite.Row
    return sql

def my_database():
    if not hasattr (g,'sqlite'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g. 'sqlite_db'):
    g.sqlite_db.close()


@app.route('/')
def index():
    return'<h1>hello , world</h1>'


@app.route('/users')
def viewusers():
    db = get_db()
    cursor = db.executes('SELECT id ,name ,age FROM user')
    return = cursor.fetchall()
    return f"<h1>"the id is {results[0]['id']}. <br> The name is {results[0]['name']}.<br> The age is {results[0]['age']}

if __name__== '__main__':
    app.run(debug=True)
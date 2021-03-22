import sqlite3
from flask import Flask, request, jsonify
from flask_mail import Mail, Message

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 500
app.config['MAIL_USERNAME'] = 'lelethundidi@gmail.com'
app.config['MAIL_PASSWORD'] = 'sunshine2'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_users_table():
    connect = sqlite3.connect('book.db')
    print("Databases has opened")

    connect.execute(
        'CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT, email_address TEXT, phone INTEGER, Adults INTEGER, Children INTEGER,  Checkin TEXT ,Checkout TEXT, DISH TEXT, RATE TEXT )')
    print("Users Table was created successfully")
    print(connect.execute("info table_info('users')").fetchall())

    connect.close()

create_users_table()

@app.route('/')
@app.route('/add/', methods=['POST', 'GET'])
def add_users():
    if request.method == 'POST':
        try:

            fullname = request.form['customer_name']
            email_address = request.form['customers_email']
            phone = request.form['visitor_phone']
            Adults = request.form['total_adults']
            Children = request.form['total_children']
            Checkin = request.form['checkin']
            Checkout = request.form['checkout']
            DISH = request.form['dish']
            RATE = request.form['text']

            # username = request.form['username']
            # password = request.form['password']
            # confirm_password = request.form['confirm']
            # email = request.form['email']

            if fullname == fullname:
                with sqlite3.connect('book.db') as con:
                    cursor = con.cursor()
                    cursor.execute(
                        "INSERT INTO users (fullname, email_address, phone, Adults, Children ,Checkin ,Checkout , DISH ,RATE) VALUES (?, ?, ?, ?, ?,?,?,?,?)",
                        (fullname, email_address, phone, Adults, Children, Checkin, Checkout, DISH, RATE))
                    con.commit()
                    msg = fullname + " was added to the databases"
                    row_id = cursor.lastrowid
                    cancellation_link = "<a href='{link}'>link</a>".format(
                        link="https://shielded-retreat-11649.herokuapp.com/delete/" + str(row_id) + "/")
                    send_mail(fullname, email_address, Adults, Children, Checkin, Checkout, DISH, cancellation_link)

                    return jsonify(msg)
        except Exception as e:
            con.rollback()
            msg = "Error occured in insert " + str(e)
        finally:

            con.close()
        return jsonify(msg=msg)

        finally:

            con.close()
        return jsonify(msg=msg)


@app.route('/show-bookers/', methods=['GET'])
def show_bookers():
    users = []
    try:
        with sqlite3.connect('book.db') as connect:
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
    except Exception as e:
        connect.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        connect.close()
        return jsonify(users)


@app.route
# message object mapped to a particular URL ‘/’
@app.route('/mail/')
def index():
    msg = Message(
        "Hello Jazz",
        sender='lelethundidi@gmail.com',
        recipients=['lelethundidi@gmail.com']
    )
    msg.body = 'Hello Flask message'
    mail.send(msg)
    return 'Sent'


def send_mail(fullname, email_address, Adults, Children, Checkin, Checkout, DISH, cancellation_link):
    msg = Message(
        "Confirm your booking",
        sender=email_address,
        recipients=[email_address]
    )
    msg.body = """
        Hey {fullname},

        Your {food} is ready for you.

        Thank you for booking at Simo Dining for {no_adults} adults and {children} children on {checkin} :{checkout}

        email {email}
        we can't wait to see you !!

        This link is to cancel your reservation {link} here or call this number +27815811192

    """.format(fullname=fullname, email=email_address, no_adults=Adults, children=Children, checkin=Checkin,
               checkout=Checkout, book=DISH, link=cancellation_link)
    mail.send(msg)

@app.route('/delete/<int:user_id>/', methods=["GET"])
def delete_user(user_id):
    msg = None
    try:
        with sqlite3.connect('book.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM users WHERE user_id=" + str(user_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting the user in the database: " + str(e)
    finally:
        con.close()
        return jsonify(msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
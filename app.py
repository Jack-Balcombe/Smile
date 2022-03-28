from flask import Flask, render_template, request, session, redirect
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt

DB_NAME = "C:/Users/18062/PycharmProjects/Smile/smile.db"

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "neveraskusaboutfrownbrew"


# creates a connection to the database
# inputs: database file
# outputs: the connection to the db or none.
def create_connection(db_file):
    """ create a connection to the sqlite db"""
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


@app.route('/')
def render_homepage():
    """

    :return: TBA
    """
    return render_template('home.html', logged_in=is_logged_in())


@app.route('/menu')
@app.route('/menu/<products>')
def render_menu_page():
    """

    :return: TBA
    """
    con = create_connection(DB_NAME)
    query = "SELECT name, description, volume, price, image FROM product"

    cur = con.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    con.close()

    return render_template('menu.html', products=product_list, logged_in=is_logged_in())


@app.route('/contact')
def render_contact_page():
    """

    :return: TBA
    """
    return render_template('contact.html', logged_in=is_logged_in())


@app.route('/login', methods=['GET', 'POST'])
def render_login_page():
    """

    :return: TBA
    """
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email').strip().lower()
        password = request.form.get('password').strip()

        con = create_connection(DB_NAME)
        query = """SELECT id, fname, password FROM customer WHERE email = ? """
        cur = con.cursor()
        cur.execute(query, (email,))
        user_data = cur.fetchall()
        con.close()

        try:
            user_id = user_data[0][0]
            first_name = user_data[0][1]
            db_password = user_data[0][2]
        except IndexError:
            return redirect("/login?error=Email+invalid+or+password+incorrect")

        if not bcrypt.check_password_hash(db_password, password):
            return redirect(request.referrer + "?error=Email+invalid+or+password+incorrect")

        session['email'] = email
        session['user_id'] = user_id
        session['first_name'] = first_name
        print(session)
        return redirect('/')
    return render_template('login.html', logged_in=is_logged_in())


@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    """

    :return: TBA
    """
    if request.method == 'POST':
        print(request.form)
        fname = request.form.get('fname').strip().title()
        lname = request.form.get('lname').strip().title()
        email = request.form.get('email').strip().lower()
        password = request.form.get('pass')
        password2 = request.form.get('pass2')

        if password != password2:
            return redirect('/signup?error=Passwords+do+not+match')

        if len(password) < 8:
            return redirect('/signup?error=Password+must+be+8+characters+or+more')

        hashed_password = bcrypt.generate_password_hash(password)

        con = create_connection(DB_NAME)
        query = "INSERT INTO customer(id, fname, lname, email, password) VALUES (NULL, ?, ?, ?, ?)"
        cur = con.cursor()

        try:
            cur.execute(query, (fname, lname, email, hashed_password))
        except sqlite3.IntegrityError:
            return redirect('/signup?error=email+is+already+in+use')
        con.commit()
        con.close()
        return redirect('/login')

    return render_template("signup.html")


def is_logged_in():
    """

    :return: TBA
    """
    if session.get("email") is None:
        print("not logged in")
        return False
    print("logged in")
    return True


app.run(host='0.0.0.0')

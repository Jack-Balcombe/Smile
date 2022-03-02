from flask import Flask, render_template, request, session

app = Flask(__name__)


@app.route('/')
def render_homepage():
    """

    :return: TBA
    """
    return render_template('home.html')


@app.route('/menu')
def render_menu_page():
    """

    :return: TBA
    """
    return render_template('menu.html')


@app.route('/contact')
def render_contact_page():
    """

    :return: TBA
    """
    return render_template('contact.html')


app.run(host='0.0.0.0')

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

# app.config['SECRET_KEY'] = "SECRET!"
# debug = DebugToolbarExtension(app)


@app.route('/')
def home_redirect():

    return redirect('/users')


@app.route('/users')
def home():

    users = User.query.all()
    return render_template(
        'home.html',
        users=users
    )
    # show users, list of users, button to add users


@app.route('/users/new')
def add_user():

    return render_template(
        'create_user.html'
    )


@app.route('/users/new', methods=["POST"])
def create_user():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    link = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=link)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user(user_id):

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user():
    first_name = request.form['edit_first_name']
    last_name = request.form['edit_last_name']
    link = request.form['edit_image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=link)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/{{user.id}}/edit')
def link_edit():

    return render_template("edit_user.html")

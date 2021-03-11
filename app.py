from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

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
        'create_user.html',
    )


@app.route('/users/new', methods=["POST"])
def create_user():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    link = request.form['image_url']

    if not link:
        link = None

    user = User(first_name=first_name, last_name=last_name, image_url=link)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    # post = Post.query.filter(Post.user_id == user_id).all()
    post = user.posts
    return render_template("detail.html", user=user, post=post)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['edit-first_name']
    user.last_name = request.form['edit-last_name']
    user.image_url = request.form['edit-image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/edit')
def link_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/posts/new')
def show_new_post(user_id):

    user = User.query.get_or_404(user_id)

    return render_template(
        "create_post.html",
        user=user
    )

@app.route('/users/<int:user_id>/post/new', methods=["POST"])
def submit_new_post(user_id):
    title = request.form['post-title']
    content = request.form['post-content']

    post = Post(title=title, content=content, user_id=user_id)
    # user.posts.append(post)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    user = User.query.get_or_404(user_id)

    return render_template(
        "post_detail.html",
        post = post,
        user_id = user_id,
        user = user
    )

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['edit-title']
    post.content = request.form['edit-content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route('/posts/<int:post_id>/edit')
def link_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    return render_template(
        "edit_post.html",
        user_id=user_id,
        post=post)

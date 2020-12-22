"""Blogly application."""

from flask import Flask, render_template, redirect, request, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)

# USER ROUTES
@app.route('/')
def home_posts():
    posts = Post.query.order_by(Post.create_at.desc()).limit(5).all()
    return render_template('posts/home.html', posts = posts)

@app.errorhandler(404) 
def invalid_route(e): 
    """handle error page"""
    return render_template('404.html'), 404

@app.route('/users')
def home_page():
    """Show all of users"""
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('users/list.html', users = users)

@app.route('/users', methods=["POST"])
def add_user():
    """Put new user into the list"""
    first_name = request.form.get('first')
    last_name = request.form.get('last')
    image_url = request.form.get('image')

    if ((first_name == '') or (last_name == '') or (image_url == '')):
        flash('Please fill out the missing part.', 'err')
        return redirect(url_for('add_form'))

    new_user = User(first_name = first_name, last_name = last_name, img_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

# @app.route('/users')
# def show_users():
#     """Show all of users"""
#     return redirect('/')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about an user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template('users/detail.html', user = user, posts = posts)

@app.route('/users/new')
def add_form():
    """Create a new user form"""
    return render_template('users/create.html')

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    """Edit form for a user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def save_edit(user_id):
    """Save edited information for an existing user"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form.get('first')
    user.last_name = request.form.get('last')
    user.img_url = request.form.get('image')

    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete the current user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

# POST ROUTES

@app.route('/posts/<int:post_id>')
def title_detail(post_id):
    """Show all the posts"""
    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('posts/detail.html', post = post, user = user)

@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Add a new post"""
    user = User.query.get_or_404(user_id)
    return render_template('posts/create.html', user = user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_detail(user_id):
    """Show the post detail """
    title = request.form.get('title')
    content = request.form.get('content')
    user = User.query.get_or_404(user_id)

    if ((title == '') or (content == '') or (user == '')):
        flash('Please fill out the missing part.', 'err')
        return redirect(f'/users/{user_id}/posts/new')

    new_post = Post(title = title, content = content, user = user)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('posts/edit.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods = ['Post'])
def save_post(post_id):
    post = Post.query.get_or_404(post_id)

    post.title = request.form.get('title')   
    post.content = request.form.get('content')

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete the current user"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')
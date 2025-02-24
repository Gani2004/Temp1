from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from Blog_Project.app.models import BlogPost, db
from Blog_Project.app.forms import BlogPostForm

bp = Blueprint('blog', __name__)

@bp.route('/')
@login_required
def index():
    posts = BlogPost.query.all()
    return render_template('index.html', posts=posts, current_user=current_user)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_post = BlogPost(title=title, content=content, user_id=current_user.id)  # Link post to user
        db.session.add(new_post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('blog.index'))
    return render_template('create_post.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/post/<int:post_id>')
def view_post(post_id):
    # Logic to retrieve and display the post
    post = BlogPost.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)

@bp.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        # Assign current_user to the new blog post
        post = BlogPost(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog.index'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@bp.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    try:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting post: ' + str(e), 'danger')

    return redirect(url_for('blog.index'))
from Blog_Project.app.models import User
@bp.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html',users=all_users)
# Removed duplicate route for /create to avoid conflicts

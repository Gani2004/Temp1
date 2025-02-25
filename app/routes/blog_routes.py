from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import BlogPost, db
from app.forms import BlogPostForm
import jsonify

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
from app.models import BlogPost,Comment
@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    # Handle comment submission
    if request.method == 'POST':
        comment_content = request.form.get('comment')
        if comment_content.strip():
            new_comment = Comment(content=comment_content.strip(), user_id=current_user.id, post_id=post.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added!', 'success')
            return redirect(url_for('blog.view_post', post_id=post.id))
        else:
            flash('Comment cannot be empty.', 'warning')

    # Fetch comments for display
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).all()
    return render_template('view_post.html', post=post, comments=comments)

@bp.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    post.likes += 1
    db.session.commit()
    return jsonify({'likes': post.likes})


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
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    # Check if the current user is the author
    if post.user_id != current_user.id:
        flash("You don't have permission to delete this post.", 'danger')
        return redirect(url_for('blog.view_post', post_id=post.id))

    # Proceed with deletion
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting post: ' + str(e), 'danger')

    return redirect(url_for('blog.index'))

from app.models import User
@bp.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html',users=all_users)
# Removed duplicate route for /create to avoid conflicts

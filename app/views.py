from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import SignupForm, LoginForm, SupportForm
from app.models import User, Page, SupportClaim
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('page', page_id=current_user.last_page_id or 1))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('page', page_id=1))
    return render_template('signup.html', title='Sign Up', form=form, show_progress=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('page', page_id=current_user.last_page_id or 1))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('page', page_id=user.last_page_id or 1)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, show_progress=False)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('page', page_id=current_user.last_page_id or 1))
    return render_template('home.html', title='Home', show_progress=False)

@app.route('/about')
def about():
    return render_template('about.html', title='About', show_progress=False)

@app.route('/support', methods=['GET', 'POST'])
def support():
    form = SupportForm()
    if form.validate_on_submit():
        support_claim = SupportClaim(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(support_claim)
        db.session.commit()
        flash('Your support claim has been submitted.', 'success')
        return redirect(url_for('support'))
    return render_template('support.html', title='Support', form=form)

@app.route('/page/<int:page_id>', methods=['GET', 'POST'])
@login_required
def page(page_id):
    page = Page.query.get_or_404(page_id)
    current_user.last_page_id = page_id
    db.session.commit()
    total_pages = Page.query.count()
    progress = round((page_id / total_pages) * 100)
    return render_template(page.template_name, title=page.title, progress=progress, show_progress=True)
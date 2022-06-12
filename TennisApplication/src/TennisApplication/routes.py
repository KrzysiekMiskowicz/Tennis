import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from src.TennisApplication.forms import RegistrationForm, LoginForm, UpdateAccount
from src.TennisApplication import app, db, bcrypt
from src.TennisApplication.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    first_name=form.first_name.data, last_name=form.last_name.data, birth_date=form.birth_date.data,
                    phone_number=form.phone_number.data, city=form.city.data)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} created account! You are able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unsuccessful login. Check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', 'profile_pictures', picture_name)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_name = save_picture(form.picture.data)
            current_user.image_file = picture_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.birth_date = form.birth_date.data
        current_user.phone_number = form.phone_number.data
        current_user.city = form.city.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.birth_date.data = current_user.birth_date
        form.phone_number.data = current_user.phone_number
        form.city.data = current_user.city
    image_file = url_for('static', filename=os.path.join('profile_pictures', current_user.image_file))
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/reservation", methods=['GET', 'POST'])
def reservation():
    reservations = (14, 17, 20)
    return render_template('reservation.html', title='Reservation', reservations=reservations)

from types import NoneType
from db_forms import *
import email_validator
# from blueman.bluez.obex.Session import Session
from flask import Flask, render_template, flash, request, make_response, redirect, url_for, send_from_directory, abort, jsonify
from werkzeug.utils import secure_filename
from markupsafe import Markup
from flask_wtf.csrf import CSRFProtect
import os, uuid, flask_login
from sqlalchemy import  create_engine, or_, and_, func
from sqlalchemy.orm import sessionmaker
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '385fc8dde4551bddd973d217'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
csrf = CSRFProtect(app)
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

engine = create_engine("sqlite:///webnotes.db")
Session = sessionmaker(bind=engine)


@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# def get_user():
#     user_id = request.cookies.get('user_id')
#     if user_id:
#         with Session() as db:
#             user = db.query(Users).filter_by(id=user_id).first()
#             print(user.id)
#         if user:
#             name = user.first_name
#             return name
#         else:
#             return False
#     else:
#         return False

# def file_upload(file):
#     if file and allowed_file(file.filename):
#         secure_name = secure_filename(file.filename)
#         name, ext = os.path.splitext(secure_name)
#         truncated_name = name[:5]
#         unique_id = uuid.uuid4().hex[:8]
#         filename = f"{truncated_name}_{unique_id}{ext}"
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return filename
#     else:
#         return None

@app.route('/')
def index():
    # username = get_user()
    username = False
    return render_template('index.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # username = get_user()
    username = False
    if request.method == 'POST' and form.validate():
        login_str = form.login.data
        password_str = form.password.data
        with Session() as db:
            user = db.query(Users).filter(and_(Users.login == login_str, Users.password_ == password_str)).first()
        if user:
            if user.login == login_str and user.password_ == password_str:
                flash(Markup('<h3>Вы успешно зашли в аккаунт</h3>'))
                flash(Markup(f'<p>Имя: {user.login}</p><p>Тип аккаунта: {user.account_type}</p>'))
                # response = make_response(render_template('login_msg.html', form=form, username=username))
                # response.set_cookie('user_id', str(user.id), max_age=60 * 60 * 24)
                # return response
        else:
            flash(Markup('<h3>Неверное имя пользователя или пароль</h3>'))

    return render_template('log_reg.html', type='login', form=form, page_name='Вход', username=username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # username = get_user()
    username = False
    if request.method == 'POST' and form.validate():
        login_str = form.login.data
        e_mail_str = form.e_mail.data
        password_str = form.password.data
        with Session() as db:
            user = db.query(Users).filter(or_(Users.login == login_str, Users.e_mail == e_mail_str)).first()
        if user:
            if user.login == login_str or user.e_mail == e_mail_str:
                flash(Markup('<h3>Такой пользователь уже существует</h3>'))
        else:
            with Session() as db:
                new_user = Users(login=login_str, e_mail=e_mail_str, password_=password_str)
                db.add(new_user)
                db.commit()
            flash(Markup('<h3>Пользователь успешно создан</h3>'))

    return render_template('log_reg.html', type='register', form=form, page_name='Регистрация', username=username)

@app.route('/logout')
def logout():
    pass
    # response = make_response(redirect(url_for('index')))
    # response.set_cookie('user_id', '', expires=0)
    # return response

if __name__ == '__main__':
    app.run(debug=True)
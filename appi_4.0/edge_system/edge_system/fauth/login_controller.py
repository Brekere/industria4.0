#import re
from flask import Blueprint, render_template, flash, url_for, request, session
from flask_login import logout_user, login_user, current_user
from werkzeug.utils import redirect
import requests


from edge_system import db, remote_server
from edge_system.fauth.model.users import LoginForm, UsersLogin, RegisterForm, get_idx_choice, get_key_choice, get_description_choice
from edge_system import login_manager

fauth = Blueprint('fauth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return UsersLogin.query.get(user_id)


@fauth.route('/users/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(meta={'csrf': False})
    id_remote_user = -1
    if '_remote_id' in session:
        print(session)
        form.fullname.data = session['_full_name']
        form.id_role.data = get_key_choice(session['_id_role'])
        form.id_employee.data = session['_id_employee']
        id_remote_user = session['_remote_id']
        if UsersLogin.query.filter_by(id_employee = form.id_employee.data).first():
            flash("Employee already registered!!")
    
    if form.validate_on_submit():
        if UsersLogin.query.filter_by(id_employee = form.id_employee.data).first():
            flash("Employee already registered!!")
        else:
            id_role = get_idx_choice(form.id_role.data)
            user = UsersLogin(
                username=form.username.data, 
                fullname=form.fullname.data, 
                pwhash=form.password.data,
                id_employee=form.id_employee.data, 
                id_role=id_role,
                id_remote_user=id_remote_user,
                role=get_description_choice(id_role)
            )
            db.session.add(user)
            db.session.commit()
            flash("Successfully registered employee!!")
        return redirect(url_for('home.home_page'))
    
    if form.errors:
        flash(form.errors, 'danger')

    return render_template('fauth/register.html', form = form)


@fauth.route('/users/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('User already authenticated')
        return redirect(url_for('home.home_page'))
    form = LoginForm(meta={'csrf': False})
    if form.validate_on_submit():
        user = UsersLogin.query.filter_by(username = form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome ' + user.fullname)
            next = request.form['next']
            #if not is_safe_url(next):
            #    return abort(400)
            return redirect(next or url_for('machine.info'))
        else:
            flash('Error: Wrong password or user', 'danger')
            return redirect(url_for('fauth.login'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('fauth/login.html', form = form)

@fauth.route('/users/logout')
def logout():
    logout_user()
    flash('Closed session!!')
    return redirect(url_for('fauth.login'))


@fauth.route('/remote_validation', methods=['GET', 'POST'])
def remote_login():
    if current_user.is_authenticated:
        flash('User already authenticated')
        return redirect(url_for('home.home_page'))
    form = LoginForm(meta={'csrf': False})
    if form.validate_on_submit():
        url_user = remote_server + 'json/usuario/login'
        print(':::::: ', form.username.data, form.password.data)
        payload = {'username': form.username.data, 'password': form.password.data}
        try:
            response = requests.post(url_user, data=payload) 
        except :
            flash('User or password are incorrect', 'danger')
            return redirect(url_for('home.home_page')) 
        print("*************************************** POST")
        json_data = response.json()
        if 'usuario' in json_data:
            user_data = json_data['usuario']
            print(user_data)
            session['_remote_id'] = user_data['id']
            session['_full_name'] = user_data['full_name']
            session['_id_role'] = 1 # falta recibir este parametro de la api
            session['_id_employee'] = 15428 # falta recibir este parametro de la api
            return redirect(url_for('fauth.register')) 
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('fauth/remote_login.html', form = form) 
    
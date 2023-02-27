from random import choices
from edge_system import db

from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, HiddenField, IntegerField, SelectField
from wtforms.validators import EqualTo, InputRequired
#import enum

choices_roles = [('1','Gerente General'), 
            ('2','Gerente de piso'), 
            ('3','Ingeniero de Producción'), 
            ('4','Ingeniero de Mantenimiento'), 
            ('5','Operador'), ]

def get_description_choice(idx):
    if choices_roles is not None:
        if idx < len(choices_roles) and idx > 0:
            l, c = choices_roles[idx - 1]
            return c 

def get_key_choice(idx):
    #print('idx::::', idx)
    if choices_roles is not None:
        if idx < len(choices_roles) and idx > 0:
            l, c = choices_roles[idx - 1]
            return l
    return None

def get_idx_choice(label):
    #print('label::::', label)
    if choices_roles is not None:
        for i in range(len(choices_roles)):
            l, t = choices_roles[i]
            if label == l:
                print(l)
                return i+1 # en la base de datos se almacenan de 1 en adelante ... 
    return -1


class UsersLogin(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40))
    fullname = db.Column(db.String(256))
    pwhash = db.Column(db.String(256))
    id_employee = db.Column(db.Integer) # va a tener relación con el id
    id_role  = db.Column(db.Integer) # Operador, encargado de línea o mantenimiento
    ## nuevos ... 
    id_remote_user = db.Column(db.Integer) # -1 if it is only local ... 
    role = db.Column(db.String(80))

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, username, fullname, pwhash, id_employee, id_role, id_remote_user, role):
        self.username = username
        self.fullname = fullname
        self.pwhash = generate_password_hash(pwhash)
        self.id_employee = id_employee
        self.id_role = id_role
        self.id_remote_user = id_remote_user
        self.role = role
        pass

    def __repr__(self):
        return 'User : %r' % (self.username)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

class RegisterForm(FlaskForm):
    username = StringField('User', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    fullname = StringField('Full name', validators = [InputRequired()])
    id_employee = IntegerField('Employee id', validators = [InputRequired()])
    id_role  = SelectField('Role id', validators = [InputRequired()], choices=choices_roles)
    confirm  = PasswordField('Repeat password')


class LoginForm(FlaskForm):
    username = StringField('User', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    next = HiddenField('next')

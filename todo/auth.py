
# página de autentificación

from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session, g
    )

from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from todo import db


bp = Blueprint('auth', __name__, url_prefix='/auth')


# ruta
@bp.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username, generate_password_hash(password))

        error = None

        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))  
        else:
            error = f'El usuario {username} ya está registrado'

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        # Validar datos
        user = User.query.filter_by(username = username).first()
        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña incorrecta'

        # Iniciar sesión
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('todo.index'))  
        
        flash(error)   
    return render_template('auth/login.html')


# Mantener sesión iniciada
@bp.before_app_request   # decorador que permite registrar la funcion (def load_logged_in_user) para q se ejecute en cada petición
def load_logged_in_user():
    user_id = session.get('user_id') # se obtiene el id con el cual a ingresado el usuario y se guarda en (user_id)

    if user_id is None: # si es none(nulo) es pq nadie a empezado sesión
        g.user = None # en el objeto g.user se guarda un valor nulo pq nadie a empezado sesión
    else:
        g.user = User.query.get_or_404(user_id) # se genera una consulta en la base de datos 
        #buscando el id de usuario y retorna un usuario y se guarda en el objeto g.user, de lo contrario devuelve un error de 404


# Cerrar sesión
@bp.route('/logout') # ruta
def logout(): # vista
    session.clear()
    return redirect(url_for('index'))


# Requiere autentificación

import functools

def login_required(view):    
     @functools.wraps(view)   # función decoradora
     def wrapped_view(**kwargs): # función anidada con argumentos indefinidos
         if g.user is None: # verifica si un usuario ha iniciado sesión - es nulo cuando NO ha iniciado sesión
            return redirect(url_for('auth.login')) # redirecciona a pág. de login
         return view(**kwargs) # SI ha iniciado sesión retorna vista original con argumentos indefinidos
     return wrapped_view  # es lo que retorna la función (def login_required(view))



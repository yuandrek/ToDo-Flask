

                                   # administración de Vistas


from flask import Blueprint, render_template, redirect, request, url_for, g

from todor.auth import login_required

from .models import Todo, User
from todor import db

bp = Blueprint('todo', __name__, url_prefix='/todo')



# para listar tareas

@bp.route('/list')   # ruta
@login_required     # decorador - indica q se requiere iniciar sesión
def index():       # vista
    todos = Todo.query.all()  # recupera todo
    return render_template('todo/index.html', todos = todos)


# para crear tareas

@bp.route('/create', methods=('GET', 'POST'))
@login_required     # decorador - indica q se requiere iniciar sesión
def create():
    if request.method == 'POST':
        title = request.form['title'] # datos del formulario capturados desde la base de datos
        desc = request.form['desc']   # datos del formulario capturados desde la base de datos

        todo = Todo(g.user.id, title, desc) # manera q se crea una tarea - se captura el id de la persona q inició sesión
        
        # guardar en la base de datos:
        db.session.add(todo)    # añade
        db.session.commit()     # 
        return redirect(url_for('todo.index'))
    return render_template('todo/create.html')



# para editar las tareas

def get_todo(id):     # función para retornar una TAREA mediante un id
    todo = Todo.query.get_or_404(id) # busca la tarea; si no encuentra en lista de tarea devuelve un error 404
    return todo # devuelve la tarea q se está buscando


# se crea la Vista de editar

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):  
      
    todo = get_todo(id) # utiliza la función (get_todo) para buscar en la base de datos la tarea con el id

    if request.method == 'POST':
        todo.title = request.form['title'] # modifica los datos
        todo.desc = request.form['desc']   # modifica los datos
        todo.state = True if request.form.get('state') == 'on' else False

        # guardar en la base de datos:
        db.session.commit()     # se realiza los cambios en la base de datos
        return redirect(url_for('todo.index'))
    return render_template('todo/update.html', todo = todo)


# para eliminar una tarea

@bp.route('/delete/<int:id>')  # se requiere recibir un id
@login_required
def delete(id):  # función para eliminar la tarea
    todo = get_todo(id)     # busca el id ingresado
    db.session.delete(todo) # se envia el id de la tarea recibido para borrarla
    db.session.commit()     # se envia modificación a la base de datos
    return redirect(url_for('todo.index'))
      
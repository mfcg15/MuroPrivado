from flask import render_template, request, redirect, session
from _app.models.usuario import Usuario
from _app.models.muro import Muro
from _app.models.mensaje import Mensaje
from _app import app
from flask import flash

from  flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    if 'idUsuario' in session:
        return redirect('/dashboard')
    else:
        return render_template('index.html')

@app.route("/dashboard")
def result():
    if 'idUsuario' in session:
         data = {"id": int(session['idUsuario'])}
         idusuario = int(session['idUsuario'])
    else:
        return redirect('/')

    usuario = Usuario.get_usuario(data)
    all_usuarios = Usuario.get_usuarios(data)
    cant_mensaje = Usuario.get_count_mensajes(data)
    emisores = Usuario.get_emisores(data)
    cant_men_enviados = Usuario.get_count_mensajes_emitidos(data)
    return render_template('dashboard.html', usuario = usuario, all_usuarios = all_usuarios, idusuario = idusuario, 
    cant_mensaje = cant_mensaje, all_emisores = emisores, cant_men_enviados = cant_men_enviados)

@app.route('/create_usuario', methods=["POST"])
def usuarioNew():
    if not Usuario.validate_user(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pwd
    }

    id = Usuario.save(data)

    session['idUsuario'] = id

    return redirect('/dashboard')

@app.route('/ingresar_usuario', methods=["POST"])
def usuarioShow():
    if not Usuario.validate_user_login(request.form):
        return redirect('/')

    usuario = Usuario.search_email(request.form)

    if not usuario:
        flash("Email don't exists!", 'login')
        return redirect('/')
 
    if not bcrypt.check_password_hash(usuario["password"],request.form["password"]):
        flash("Wrong Password", 'login')
        return redirect('/')

    session['idUsuario'] = usuario["id"]
    return redirect('/dashboard')

@app.route('/create_mensaje', methods=["POST"])
def newMensaje():
    dataMuro = {
        "emisor_id": request.form["emisor_id"],
        "receptor_id": request.form["receptor_id"]
    }
    print(dataMuro)
    dataMensaje = {
        "mensaje": request.form["mensaje"],
        "muro_id": Muro.save(dataMuro)
    }

    if not Mensaje.validate_mensaje(request.form):
        return redirect('/dashboard')

    Mensaje.save(dataMensaje)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def deleteMensaje(id):
    data = {"id": int(id)}
    Mensaje.delete_mensaje(data)
    return redirect('/dashboard')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
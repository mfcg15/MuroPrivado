from _app.config.connection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETRAS_REGEX = re.compile(r'^(?=.{2,}$)[a-zA-Z0-9.+_-]+$')
PASSWORD_REGEX = re.compile(r'^(?=.{8,}$)[a-zA-Z0-9]+$')

class Usuario:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO usuarios (first_name, last_name, email, password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        idUsuario = connectToMySQL('esquema_muro').query_db( query, data)
        return idUsuario

    @staticmethod
    def validate_user(data):
        is_valid = True

        if not LETRAS_REGEX.match(data['first_name']):
            flash('First name must be at least 3 characters', 'registro')
            is_valid = False
        if not LETRAS_REGEX.match(data['last_name']):
            flash('Last name must be at least 3 chatacters', 'registro')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email", 'registro')
            is_valid = False
        if  not PASSWORD_REGEX.match(data['password']):
            flash('Password must be at least 8 characters', 'registro')
            is_valid = False
        if data['password'] != data['cont_password']:
            flash("Passwords aren't the same", 'registro')
            is_valid = False

        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL('esquema_muro').query_db(query,data)
        if len(results) >= 1:
            flash('Email already exists!', 'registro')
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_user_login(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid Email', 'login')
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash('Password must be at least 8 characters', 'login')
            is_valid = False
        return is_valid

    @classmethod
    def search_email(cls, data):
        query = "SELECT * FROM usuarios where email = %(email)s;"
        result = connectToMySQL('esquema_muro').query_db(query,data)
        if len(result) < 1:
            return False
        else :
            usuario = result[0]
            return usuario
    
    @classmethod
    def get_usuario (cls, data):
        query = "SELECT * FROM usuarios where id = %(id)s;"
        result = connectToMySQL('esquema_muro').query_db(query,data)
        usuario = []
        for i in result:
            usuario.append(i)
        return usuario
    
    @classmethod
    def get_usuarios (cls, data):
        query = "SELECT * FROM usuarios where usuarios.id not in (select usuarios.id where usuarios.id = %(id)s) order by first_name asc;"
        result = connectToMySQL('esquema_muro').query_db(query,data)
        usuarios = []
        for i in result:
            usuarios.append(i)
        return usuarios
    
    @classmethod
    def get_count_mensajes (cls, data):
        query = "SELECT count(mensaje) FROM muros inner join mensajes on muros.id = mensajes.muro_id where muros.receptor_id = %(id)s;"
        result = connectToMySQL('esquema_muro').query_db(query,data)
        return result[0]["count(mensaje)"]
    
    @classmethod
    def get_emisores (cls, data):
        query = "SELECT concat(usuarios.first_name, ' ',usuarios.last_name) as emisores, mensajes.id ,mensajes.mensaje, TIMESTAMPDIFF(second,mensajes.created_at,now()) as tiempo FROM usuarios inner join muros on usuarios.id = muros.emisor_id inner join mensajes on muros.id = mensajes.muro_id where muros.receptor_id = %(id)s;"
        result = connectToMySQL('esquema_muro').query_db(query,data)
        emisores = []
        cont = 0
        for i in result:
            emisores.append(i)
        for elemt in emisores:
            for k,v in elemt.items():
                if(k == "tiempo"):
                    tiempo, timeof = Tiempo(int(v))
                    emisores[cont][k] = str(tiempo)+timeof
            cont +=1
        return emisores
    
    @classmethod
    def get_count_mensajes_emitidos (cls, data):
        query = "SELECT count(mensaje) FROM muros inner join mensajes on muros.id = mensajes.muro_id where muros.emisor_id = %(id)s;"
        result = connectToMySQL('esquema_muro').query_db(query,data)
        return result[0]["count(mensaje)"]


def Tiempo (tiempo):
    auxtiempo = tiempo

    dias = tiempo//(24*60*60)
    segundos = tiempo % (24*60*60)
    horas = segundos//(60*60)
    segundos = segundos % (60*60)
    minutos = segundos//60

    if auxtiempo <= 60:
        return auxtiempo," seconds"
    elif auxtiempo <= 3600:
        return minutos, " minutes"
    elif auxtiempo <= 86400:
        return horas, " hours"
    else:
        return dias, " days"
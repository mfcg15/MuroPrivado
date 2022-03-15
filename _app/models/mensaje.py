from _app.config.connection import connectToMySQL
from flask import flash
import re

class Mensaje:
    def __init__( self , data ):
        self.id = data['id']
        self.mensaje = data['mensaje']
        self.muro_id = data['muro_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO mensajes (mensaje, muro_id, created_at, updated_at) VALUES (%(mensaje)s,%(muro_id)s,NOW(),NOW());"
        return connectToMySQL('esquema_muro').query_db( query, data)
    
    @staticmethod
    def validate_mensaje(data):
        is_valid = True

        if len(data['mensaje']) < 5:
            flash('Message must be at least 5 characters', 'mensaje')
            is_valid = False

        return is_valid

    @classmethod
    def delete_mensaje(cls,data):
        query = "DELETE FROM mensajes where id =  %(id)s;"
        return connectToMySQL('esquema_muro').query_db(query,data)
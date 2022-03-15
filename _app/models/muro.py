from _app.config.connection import connectToMySQL

class Muro:
    def __init__( self , data ):
        self.id = data['id']
        self.emisor_id = data['emisor_id']
        self.receptor_id = data['receptor_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def save(data):
        query = "SELECT * FROM muros WHERE emisor_id = %(emisor_id)s and receptor_id = %(receptor_id)s;"
        results = connectToMySQL('esquema_muro').query_db(query,data)
        if len(results) >= 1:
            return results[0]["id"]
        else:
            query = "INSERT INTO muros (emisor_id, receptor_id, created_at, updated_at) VALUES (%(emisor_id)s,%(receptor_id)s,NOW(),NOW());"
            idMuro = connectToMySQL('esquema_muro').query_db( query, data)
            return idMuro

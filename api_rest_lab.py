# imports das libs que iremos utlizar
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps,loads
from flask_httpauth import HTTPBasicAuth
from Users_Conection import create_Engine,users_list

app = Flask(__name__)
api = Api(app)

db_connect = create_Engine()
auth = HTTPBasicAuth()

users = users_list()

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return "ok"

    
class Registros_Sensores(Resource):
    @auth.login_required
    def get(self):
        content = loads(request.data)
        dateBegin = content['dateBegin']
        dateEnd = content['dateEnd']

        conn = db_connect.connect()
        
        query =  "SELECT * from registros_sensores where str_to_date(dia, '%%d/%%m/%%Y') >= str_to_date('{0}', '%%d/%%m/%%Y') ".format(dateBegin)
        query += "and  str_to_date(dia, '%%d/%%m/%%Y') <= str_to_date('{0}', '%%d/%%m/%%Y')".format(dateEnd)

        result = conn.execute(query)
        dados = {}
        for row in result:
            d = {"temperatura":row['temperatura'],
             "dia":row['dia'],
             "humidade":row['humidade'],
             "horario":row['horario'],
             "id_node":row['id_node'],
             "id":row['id'],
             }
            dados.update({row['id']:d})
            
        
        return jsonify(dados)

       

class Registros_Controle(Resource):
    @auth.login_required
    def get(self):
        content = loads(request.data)
        dateBegin = content['dateBegin']
        dateEnd = content['dateEnd']

        conn = db_connect.connect()
        
        query =  "SELECT * from registros_controle where str_to_date(dia, '%%d/%%m/%%Y') >= str_to_date('{0}', '%%d/%%m/%%Y') ".format(dateBegin)
        query += "and  str_to_date(dia, '%%d/%%m/%%Y') <= str_to_date('{0}', '%%d/%%m/%%Y')".format(dateEnd)

        result = conn.execute(query)
        dados = {}
        for row in result:
            d = {
             "temperatura":row['temperatura'],
             "estado":row["estado"],
             "dia":row['dia'],
             "horario":row['horario'],
             "id_node":row['id_node'],
             "id":row['id'],
             }
            dados.update({row['id']:d})
            
        
        return jsonify(dados)

class Registros_API_Temperatura(Resource):
    @auth.login_required
    def get(self):
        content = loads(request.data)
        dateBegin = content['dateBegin']
        dateEnd = content['dateEnd']

        conn = db_connect.connect()
        
        query =  "SELECT * from registros_api_temperatura where str_to_date(dia, '%%d/%%m/%%Y') >= str_to_date('{0}', '%%d/%%m/%%Y') ".format(dateBegin)
        query += "and  str_to_date(dia, '%%d/%%m/%%Y') <= str_to_date('{0}', '%%d/%%m/%%Y')".format(dateEnd)

        result = conn.execute(query)
        dados = {}
        for row in result:
            d = {
             "temperatura":row['temperatura'],
             "sensacao_termica":row["sensacao_termica"],
             "dia":row['dia'],
             "horario_registro":row['horario_registro'],
             "horario_medicao":row['horario_medicao'],
             "humidade":row['humidade'],
             "id":row['id'],
             }
            dados.update({row['id']:d})
            
        
        return jsonify(dados)

api.add_resource(Registros_Sensores, '/registros_sensores')
api.add_resource(Registros_Controle, '/registros_controle')
api.add_resource(Registros_API_Temperatura, '/registros_api_temperatura') 

if __name__ == '__main__':
    app.run()

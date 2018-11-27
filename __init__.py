from flask import Flask, jsonify, abort, request
from pymongo import MongoClient
import sys
import json
from collections import deque

app = Flask(__name__)

MONGODATABASE = "grupo52"  # nombre que DEBE tener la base de datos
MONGOSERVER = "localhost"
MONGOPORT = 27017

client = MongoClient(MONGOSERVER, MONGOPORT)


@app.route('/message_id/<int:id_message>', methods=['GET'])
def message_id(id_message):
    mongodb = client[MONGODATABASE]
    collection = mongodb.messages
    output = []

    # iteramos sobre la consulta de tipo mongo(sintaxis importante)
    for s in collection.find({"_id": id_message}, {"_id": 1,
                                                   "message": 1,
                                                   "date": 1,
                                                   "lat": 1,
                                                   "long": 1,
                                                   "receptant": 1,
                                                   "sender": 1}):
        output.append(s)  # todo se guarda en una lista

    if len(output) == 0:
        return jsonify(), 404  # en caso de falla
    else:
        return jsonify(output), 200


@app.route('/user_messages/<int:id_user>', methods=['GET'])
def user_messages(id_user):
    mongodb = client[MONGODATABASE]
    collection = mongodb.usuarios  # necesitamos las dos colecciones
    collection_1 = mongodb.messages
    output = []
    messages = []

    # primero buscamos al usuario
    for s in collection.find({"_id": id_user}, {"_id": 1,
                                                "nombre": 1,
                                                "apellido": 1,
                                                "clave": 1,
                                                "correo": 1,
                                                "edad": 1,
                                                "nombre": 1,
                                                "sexo": 1}):
        output.append(s)

    # luego buscamos todos los mensajes enviados por este usuario
    for s in collection_1.find({"sender": id_user}, {"message": 1,
                                                     "date": 1,
                                                     "lat": 1,
                                                     "long": 1,
                                                     "receptant": 1}):
        messages.append(s)

    # ordenamos los mensajes segun fecha
    smessages = sorted(messages, key=lambda k: k['date'])
    # los agregamos como atributo a nuestro unico usuario
    output[0]["messages"] = smessages
    if len(output) == 0:
        return jsonify(), 404
    else:
        # retornamos este unico usuario
        return jsonify(output[0]), 200


@app.route('/between_users/<int:id_user_1>/<int:id_user_2>', methods=['GET'])
def between_users(id_user_1, id_user_2):
    mongodb = client[MONGODATABASE]
    collection = mongodb.messages
    output = []
    messages = []

    # buscamos los mensajes que 1 envió a 2
    for s in collection.find({"sender": id_user_1,
                              "receptant": id_user_2}, {"_id": 1,
                                                        "message": 1,
                                                        "date": 1,
                                                        "lat": 1,
                                                        "long": 1,
                                                        "receptant": 1,
                                                        "sender": 1}):
        output.append(s)

    # y viceversa
    for s in collection.find({"sender": id_user_2,
                              "receptant": id_user_1}, {"_id": 1,
                                                        "message": 1,
                                                        "date": 1,
                                                        "lat": 1,
                                                        "long": 1,
                                                        "receptant": 1,
                                                        "sender": 1}):
        output.append(s)

    # los ordenamos
    noutput = sorted(output, key=lambda k: k['date'])

    if len(output) == 0:
        return jsonify(), 404
    else:
        return jsonify(noutput), 200


@app.route('/find_words/', methods=['GET'])
@app.route('/find_words/<frases>', methods=['GET'])
def find_words(frases=None):
    mongodb = client[MONGODATABASE]
    collection = mongodb.messages
    output = []
    frases = json.loads(frases)  # cargamos el diccionario con las frases
    if not frases:  # en caso de estar vacio arroja error
        return jsonify("Necesitas agregar frases para buscar"), 404
    else:
        busqueda = arreglar_frases(frases)  # lo arregla para la busqueda

    for s in collection.find({"$text": {"$search": busqueda}}, {"_id": 1,
                                                                "message": 1,
                                                                "date": 1,
                                                                "lat": 1,
                                                                "long": 1,
                                                                "receptant": 1,
                                                                "sender": 1}):
        output.append(s)

    if len(output) == 0:
        return jsonify(), 404  # en caso de falla
    else:
        return jsonify(output), 200


@app.route('/find_words_2/', methods=['GET'])
@app.route('/find_words_2/<frases>', methods=['GET'])
def find_words_2(frases=None):
    mongodb = client[MONGODATABASE]
    collection = mongodb.messages
    output = list()
    frases = json.loads(frases)  # cargamos el diccionario con las frases
    if not frases:  # en caso de estar vacio arroja error
        return jsonify("Necesitas agregar frases para buscar"), 404

    while frases:
        auxiliar = frases.pop()
        busqueda = f"\"{auxiliar}\""
        for s in collection.find({"$text": {"$search": busqueda}}, {"_id": 1,
                                                                    "message": 1,
                                                                    "date": 1,
                                                                    "lat": 1,
                                                                    "long": 1,
                                                                    "receptant": 1,
                                                                    "sender": 1}):
            output.append(s)
    noutput = list()
    for tupla in output:
        if not tupla in noutput:
            noutput.append(tupla)

    if len(noutput) == 0:
        return jsonify(), 404  # en caso de falla
    else:
        return jsonify(noutput), 200


@app.route('/not_find_words/', methods=['GET'])
@app.route('/not_find_words/<frases>', methods=['GET'])
def not_find_words(frases=None):
    mongodb = client[MONGODATABASE]
    collection = mongodb.messages
    output = []
    retorno = list()
    frases = json.loads(frases)  # cargamos el diccionario con las frases
    if not frases:  # en caso de estar vacio arroja error
        return jsonify("Necesitas agregar frases"), 404
    else:
        busqueda = arreglar_frases(frases)  # lo arregla para la busqueda

    while frases:
        auxiliar = frases.pop()
        busqueda = f"\"{auxiliar}\""
        for s in collection.find({"$text": {"$search": busqueda}}, {"_id": 1,
                                                                    "message": 1,
                                                                    "date": 1,
                                                                    "lat": 1,
                                                                    "long": 1,
                                                                    "receptant": 1,
                                                                    "sender": 1}):
            output.append(s)
    noutput = list()
    for tupla in output:
        if not tupla in noutput:
            noutput.append(tupla)

    for s in collection.find({}, {"_id": 1,
                                  "message": 1,
                                  "date": 1,
                                  "lat": 1,
                                  "long": 1,
                                  "receptant": 1,
                                  "sender": 1}):
        if s not in output:
            retorno.append(s)

    if len(retorno) == 0:
        return jsonify(), 404  # en caso de falla
    else:
        return jsonify(retorno), 200


def arreglar_frases(frases):  # funcion auxiliar que intruduce los simbolos necesarios
    frases = deque(frases)  # para la busqueda
    retorno = ""
    if len(frases) == 0:
        return None
    else:
        while frases:  # utilizaremos una cantidad no determinada de frases a ingresar
            frase = frases.popleft()
            retorno += f"\"{frase}\""
        return retorno


def arreglar_frases_2(frases):  # funcion auxiliar que intruduce los simbolos necesarios
    frases = deque(frases)  # para la busqueda
    retorno = ""
    if len(frases) == 0:
        return None
    else:
        while frases:  # utilizaremos una cantidad no determinada de frases a ingresar
            frase = frases.popleft()
            retorno += f"-\"{frase}\""
        return retorno


@app.route('/add_message/', methods=['POST'])
def add_message():
    mongodb = client[MONGODATABASE]
    collection = mongodb.messages
    # Guarda el json en el variable data
    data = request.get_json()

    if '_id' in data:
        identificador = data["_id"]
    else:
        identificador = obtener_indice()

    # Se inserta un nuevo item a la colección de mongo con los
    #  parámetros definidos en el json
    inserted_message = collection.insert_one({
        '_id': identificador,
        'message': data["message"],
        'sender': data["sender"],
        'receptant': data["receptant"],
        'lat': data["lat"],
        'long': data["long"],
        'date': data["date"],
    })
    # insert_one retorna None si no pudo insertar
    if inserted_message is None:
        return jsonify(), 404
    # Retorna el id del elemento insertado
    else:
        return jsonify({"id": str(inserted_message._id)}), 200


@app.route('/remove_message/<int:id_message>', methods=['DELETE'])
def remove_message(id_message):
    mongodb = client[MONGODATABASE]
    messages = mongodb.messages
    result = messages.delete_one({
        '_id': id_message,
    })

    if result.deleted_count == 0:
        return jsonify(), 404
    else:
        return jsonify("Eliminado"), 200


@app.route('/')
def hello_world():
    print(123, file=sys.stdout)
    return jsonify({"status": "ok"})


def obtener_indice():
    mongodb = client[MONGODATABASE]
    collection = mongodb.messages
    output = list()
    for s in collection.find({}, {"_id": 1}):
        output.append(s)

    indices = list()
    for cosa in output:
        indices.append(cosa["_id"])
    return max(indices) + 1


if __name__ == '__main__':
    # Pueden definir su puerto para correr la aplicación
    app.run(port=5000)

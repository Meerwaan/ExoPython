from flask import Flask, render_template
from flask import request
from flask import make_response
import os
from jsonschema import validate, ValidationError

schema = {
    "type" : "object",
    "properties" :{
        "fname" : {
            "type" : "string"
        },
         "lname" : {
             "type" : "string"
         },
    },
}


app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    function that display a page.

    :return:
    """
    return 'Hello World!' \
           '<a href="/page"> New Page</a>'


@app.route('/page')
def title():
    """
    a little function that display a text on a new page.

    :return: content of the page
    """
    return '<h1>Ceci est une nouvelle page</h1>'


@app.route('/users', methods=['GET'])
def get_users():
    """
    Function to display all users (names and lastnames) and adding them to a dictionnary.
    :return: a response that display all user in the website
    """
    page = int(request.args["page"])
    users = os.listdir('users')
    taille = int(request.args["taille"])
    nbPage = taille / len(users)
    # body = f'{page} / {taille} / {math.ceil(nbPage)}'
    liste = users[(page - 1) * taille:((page - 1) * taille) + taille]
    table = {}
    table['users'] = {}
    for i in liste:
       file = open('users/' + i, 'r')
       data = file.readlines()
       fname = data[0].split('\n')
       table['users'][i] = {"fname": fname[0], "lname": data[1]}
       file.close()
    body = f'{table["users"]}'
    return make_response(body,200)


@app.route('/users', methods=['POST'])
def create_user():
    """
    function that try to create a file with a name stocked in parameters, and adding name and lastname into it.
    :return: a response that display the user in the website or an error
    """
    try:
        body = request.get_json()
        fname = body["fname"]
        lname = body["lname"]
        isPresent = False
        for base, dirs, files in os.walk('users'):
            for file in files:
                if request.args["id"] in file:
                    isPresent = True
                else:
                    with open(f'users/{file}') as user:
                        stock = user.readlines()
                        name = stock[0].split('\n')
        if isPresent:
            body = "Fichier déjà présent"
        else:
            if stock[1] in lname and name[0] in fname:
                body = 'déjà renseigné'
            else:
                file = open(f'users/{request.args["id"]}.txt', 'a')
                file.write(f'{fname}\n{lname}')
                file.close()
        return make_response(body,200)
    except KeyError or TypeError:
        body = "Problème de JSON !"
        return make_response(body,200)

@app.route('/users', methods=['PATCH'])
def change_user():
    """
    function to replace text in the user's file
    :return: a response that display the user in the website or an error
    """
    try:
        body = request.get_json()
        fname = body["fname"]
        lname = body["lname"]
        isPresent = False
        for base, dirs, files in os.walk('users'):
            for file in files:
                if request.args["id"] in file:
                    isPresent = True
        if not isPresent:
            body = "Fichier n'existe pas"
        else:
            data = fname + '\n' + lname
            file = open(f'users/{request.args["id"]}.txt', 'w')
            file.write(f'{data}')
            file.close()
        return make_response(body,200)
    except KeyError or TypeError:
        body = "Problème de JSON"
        return make_response(body, 200)


@app.route('/users', methods=['DELETE'])
def delete_user():
    """
    function that delete the file of the user in params
    :return:
    """
    body = "User deleted!"
    os.remove(f'users/{request.args["id"]}.txt')
    return make_response(body, 200)


@app.errorhandler(FileNotFoundError)
def file_error(error):
    """
    function to handle FileNotFoundError in case of deleting an unexistant file
    :param error:
    :return:
    """
    return 'Le fichier est momentanément indisponible (en gros il existe pas)'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)

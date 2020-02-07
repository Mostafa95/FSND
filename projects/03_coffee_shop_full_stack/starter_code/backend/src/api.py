import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
db_drop_and_create_all()


@app.route('/drinks', methods=['GET'])
def drinks():
    # drink = Drink(title="test2",
    #               recipe='[{"color": "red2", "name":"cufe2", "parts":4}]')
    # drink.insert()
    # drink2 = Drink(title="test",
    #               recipe='[{"color": "red", "name":"cufe", "parts":2}]')
    # drink2.insert()
    data = Drink.query.all()
    if len(data) == 0:
        abort(404)
    res = [d.short() for d in data]
    return jsonify({
        'success': True,
        'drinks': res
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth(permission='get:drinks-detail')
def drinks_details(payload):
    # drink = Drink(title="test2",
    #               recipe='[{"color": "red2", "name":"cufe2", "parts":4}]')
    # drink.insert()
    # drink2 = Drink(title="test",
    #               recipe='[{"color": "red", "name":"cufe", "parts":2}]')
    # drink2.insert()
    data = Drink.query.all()
    if len(data) == 0:
        abort(404)
    res = [d.long() for d in data]
    return jsonify({
        'success': True,
        'drinks': res
    })


@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def insert_drink(payload):
    body = request.get_json()
    drink = Drink(title=body['title'], recipe=str(body['recipe']))
    try:
        drink.insert()
    except Exception:
        abort(500)

    return jsonify({
        'success': True,
        'drinks': drink.long()
    })


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def update_drink(payload, id):
    # drink = Drink(title="test3",
    # recipe="[{\"color\": \"fvdvvfd\", \"name\":\"vfdfv\", \"parts\":4}]")
    # drink.insert()

    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)

    body = request.get_json()
    if 'title' in body:
        drink.title = body['title']
    if 'recipe' in body:
        drink.recipe = body['recipe']
    drink.update()

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(payload, id):
    # drink = Drink(title="test3",
    # recipe="[{\"color\": \"fvdvvfd\", \"name\":\"vfdfv\", \"parts\":4}]")
    # drink.insert()

    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink is None:
        abort(404)

    drink.delete()
    return jsonify({
        'success': True,
        'id': id
    })


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(400)
def BadRequest(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "Bad Request"
                    }), 400


@app.errorhandler(404)
def NotFound(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "Resource not found"
                    }), 404


@app.errorhandler(500)
def InternelError(error):
    return jsonify({
                    "success": False,
                    "error": 500,
                    "message": "Internal server error"
                    }), 500


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def unauthorized(error):
    print(error.status_code)
    print(error.error)
    return jsonify({
                    "success": False,
                    "error": error.status_code,
                    "message": error.error
                    }), error.status_code

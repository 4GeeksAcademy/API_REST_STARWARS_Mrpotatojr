"""
This module handles starting the API Server, loading the DB, and adding the endpoints.
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response"
    }

    return jsonify(response_body), 200

# Only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

# Endpoints

@app.route('/people', methods=['POST'])
def add_people():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "No body provided"}), 400

    name = body.get("name")
    height = body.get("height")
    gender = body.get("gender")
    birthyear = body.get("birthyear")
    eyecolor = body.get("eyecolor")

    if not name or not height or not gender or not birthyear or not eyecolor:
        return jsonify({"msg": "Missing required fields"}), 400

    new_person = Person(
        name=name,
        height=height,
        gender=gender,
        birthyear=birthyear,
        eyecolor=eyecolor
    )
    db.session.add(new_person)
    db.session.commit()

    return jsonify(new_person.serialize()), 201

    
    
   

@app.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    results = list(map(lambda x: x.serialize(), people))
    return jsonify(results), 200


@app.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = Person.query.get(person_id)
    if person is None:
        return jsonify({"msg": "Person not found"}), 404
    return jsonify(person.serialize()), 200


@app.route('/planets', methods=['POST'])
def add_planet():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "No body provided"}), 400

    name = body.get("name")
    gravity = body.get("gravity")
    climate = body.get("climate")
    terrain = body.get("terrain")
    diameter = body.get("diameter")

    if not name or not gravity or not climate or not terrain or not diameter:
        return jsonify({"msg": "Missing required fields"}), 400

    new_planet = Planet(
        name=name,
        gravity=gravity,
        climate=climate,
        terrain=terrain,
        diameter=diameter
    )
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 201

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    results = list(map(lambda x: x.serialize(), planets))
    return jsonify(results), 200



@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    results = list(map(lambda x: x.serialize(), users))
    return jsonify(results), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"msg": "User ID not provided"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    results = list(map(lambda x: x.serialize(), favorites))
    return jsonify(results), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"msg": "User ID not provided"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"msg": "User ID not provided"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    people = Person.query.get(people_id)
    if people is None:
        return jsonify({"msg": "Person not found"}), 404
    favorite = Favorite(user_id=user_id, person_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"msg": "User ID not provided"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"msg": "User ID not provided"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    favorite = Favorite.query.filter_by(user_id=user_id, person_id=people_id).first()
    if favorite is None:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

# body:  <!--- The member's json object --> 

jackson_family.add_member(
    {
    "id": jackson_family._generate_id(),
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
    }
)
jackson_family.add_member(
    {
    "id": jackson_family._generate_id(),
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
    }
)
jackson_family.add_member(
    {
    "id": jackson_family._generate_id(),
    "first_name": "Jimmy",
    "age": 4,
    "lucky_numbers": [1]
    }
)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# get all
@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200

# get individual 
@app.route('/members/<int:id>', methods=['GET'])
def get_each_member(id):
    member = jackson_family.get_member()
    return jsonify(member), 200

# add

# delete


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

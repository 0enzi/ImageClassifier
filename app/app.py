from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.ImageRecognizer
users = db["users"]

# Helpers
def user_exists(username):
    if users.find({"Username": username}).count()==0:
        return False
    else:
        return True


class Register(Resource):
    def post(self):
        posted_data = requests.json()
        username = posted_data["username"]
        password = posted_data["password"]
        if user_exists(username):
            return jsonify({"Message": "User already registered"})
        
        hashed_pw = bcrypt.hashedpw(password.encode("utf-8"), bcrypt.gensalt(password.decode("utf-8")))

        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Credits": 27
        })

        return jsonify({"Message": "Registration successful"})

app.run(host='0.0.0.0', port="3000")
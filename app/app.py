from requests.sessions import requote_uri
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


class Classify(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        password = posted_data["password"]
        url = posted_data["url"]

        #TODO
        ret, err = auth_user(username, password)
        if err:
            return jsonify(ret)

        credits = users.find({
            "Username": username,
        })[0]["Credits"]

        if credits<=0:
            return jsonify(gen_ret_dict(303, "Insuffiecient Credits!"))
        
        r = requests.get(url)
        ret = {}

        with open("temp.jpg", "wb") as f:
            f.write(r.content)
            proc = subprocess.Popen("python3 classify_image.py --model_dir=. --image_file=./temp.jpg")
            proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                ret = json.load(g)
        
        users.update_one({"Username": username}, 
            {"$set": {
                "Credits":credits-1
            }})
        return ret
        

app.run(host='0.0.0.0', port="3000")
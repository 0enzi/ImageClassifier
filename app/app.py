from requests.sessions import requote_uri
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json

# Flask and flask_restful
app = Flask(__name__)
api = Api(app)

class Classify(Resource):
    def post(self):
        posted_data = request.get_json()
        url = posted_data["url"]
        r = requests.get(url)
        ret = {}

        with open("temp.jpg", "wb") as f:
            f.write(r.content)
            proc = subprocess.Popen("python3 classify_image.py --model_dir=. --image_file=./temp.jpg")
            proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                ret = json.load(g)
        
       
        return ret
        

app.run(host='0.0.0.0', port="3000")
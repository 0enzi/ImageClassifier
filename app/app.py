from flask import Flask, request
from flask_restful import Api, Resource
import requests
import subprocess
import json

# Flask and flask_restful
app = Flask(__name__)
api = Api(app)


# Classifies image from URL given
class Classify(Resource):
    def post(self):
        posted_data = request.get_json()
        url = posted_data["url"]
        r = requests.get(url)
        ret = {}

        with open("temp.jpg", "wb") as f:
            f.write(r.content)
            proc = subprocess.Popen(['python3','classify.py','--image','temp.jpg'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            ret = proc.communicate()[0]
            proc.wait()
            with open("text.json") as g:
                ret = json.load(g)
        
       
        return ret
        
api.add_resource(Classify, "/classify")

app.run(host='0.0.0.0', port="3000")
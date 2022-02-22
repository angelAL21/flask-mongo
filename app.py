from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI']= 'mongodb://localhost/pymongodb'

mongo= PyMongo(app)

#create user
@app.route('/users', methods=['POST'])
def create_user():
    username= request.json['username']
    email= request.json['email']
    password= request.json['password']
    
    if username and email and password:
        hashed_password=generate_password_hash(password)
        id=mongo.db.users.insert(
            {'username': username, 'email': email, 'password': hashed_password }
        )
        response={
            'id': str(id),
            'username': username,
            'email': email,
            'password': hashed_password
        }
        return response
    else:
        return not_found()
        
#get all users
@app.route('/users', methods=['GET'])
def get_users():
    user = mongo.db.users.find()
    response=json_util.dumps(user)
    return response(response, mimeype='application/json')


@app.errorhandler(404)
def not_found(error=None):
    response=jsonify({
        'message': 'resource not found: '+ request.url,
        'status': 404
    })
    response.status_code =404
    return response

if __name__ == '__main__':
    app.run(debug=True)
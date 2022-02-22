from flask import Flask, request, jsonify ,Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

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
    return Response(response, mimeype='application/json')

#get user by id.
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

#delete user by id.
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

#update user by id.
@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'username': username, 'email': email, 'password': hashed_password}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()

#error handler.
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
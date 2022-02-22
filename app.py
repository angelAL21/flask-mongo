from flask import Flask, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['MONGO_URI']= 'mongodb://localhost/pymongodb'

mongo= PyMongo(app)

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
        

@app.errorhandler(404)
def not_found(error=None):
    message={
        'message': 'resource not found: '+ request.url,
        'status': 404
    }
    return message

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'thisissecret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    input_value = db.Column(db.String(50))

@app.route('/user', methods = ['GET'])
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['email'] = user.email
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['id']= user.id
        user_data['input'] = user.input_value
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/update', methods = ['POST'])
def update():
    input_value=request.get_json()['input']
    user_id=request.get_json()['id']
    user = User.query.filter_by(id = user_id).first()

    user.input_value= input_value
    db.session.commit()

    return jsonify('updated')

@app.route('/signin', methods = ['POST'])
def get_user():
    user_email=request.get_json()['email']
    user_password=request.get_json()['password']
    
    user= User.query.filter_by(email = user_email).first()
    
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'}) 

    if (user.password == user_password):
        user_data = {}
        user_data['email'] = user.email
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['input'] = user.input_value
        user_data['id'] = user.id
        user_data['token']= 123
        return jsonify({'user' : user_data})
                
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'}) 


@app.route('/register', methods = ['POST'])
def register_user():
    user_email = request.get_json()['email']
    user_password = request.get_json()['password']
    user_name = request.get_json()['name']

    new_user = User(email = user_email, name = user_name, password = user_password, input_value = "0")
    db.session.add(new_user)
    db.session.commit()
    
    user_data = {}
    user_data['email'] = new_user.email
    user_data['name'] = new_user.name
    user_data['password'] = new_user.password
    user_data['input'] = new_user.input_value
    user_data['id'] = new_user.id
    user_data['token']= 123

    return jsonify({'user' : user_data})


if __name__ == '__main__':
    app.run(debug= True)
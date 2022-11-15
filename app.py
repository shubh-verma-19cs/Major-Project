# from random import random
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://mqtt:postgres@localhost/mqtt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CORS(app)

class User(db.Model):
    __tablename__ = 'users'
    # id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), primary_key=True)
    user_email = db.Column(db.String(100), nullable = False)
    def __repr__(self):
        return "<User %r>" % self.user_name

@app.route('/')
def index():
    return jsonify({"message":"Flask website"})

# Create
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    user_name = user_data['user_name']
    user_email = user_data['user_email']
    user = User(user_name=user_name, user_email=user_email)

    db.session.add(user)
    db.session.commit()

    return jsonify({"success":True, "response":"USer added"})

#Read
@app.route('/getusers', methods=['GET'])
def getUsers():
    all_users = []
    users = User.query.all()
    for user in users:
        results = {
            "user_name":user.user_name,
            "user_email":user.user_email,
        }
        all_users.append(results)
    return jsonify({
        "status": True,
        "users": all_users,
        "total_users": len(users),
    })

# Update
@app.route("/users/<string:user_name>", methods = ['PATCH'])
def update_user(user_name):
    user = User.query.get(user_name)
    user_email = request.json['user_email']

    if user is None:
        abort(404)
    else:
        user.user_email = user_email
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": "Updated"})

@app.route("/users/<string:user_name>", methods = ['DELETE'])
def deete_user(user_name):
    user = User.query.get(user_name)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"status": "Deleted"})

if __name__ == '__main__':
    app.run(debug=True)
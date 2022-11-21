# from random import random
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

# import bcrypt
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://majorproject:majorproject@localhost/mqtt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


CORS(app)
#  CREATE TABLE "users" (email TEXT PRIMARY KEY NOT NULL, password TEXT NOT NULL, image TEXT, name TEXT);
class User(db.Model):
    __tablename__ = 'users'
    # id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.email

class Sensor(db.Model):
    __tablename__ = 'sensors'
    sensor_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    pin = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)

    def __repr__(self):
        return "<Sensor %r>" % self.pin


@app.route('/')
def index():
    return jsonify({"message": "Flask website"})


@app.route('/login', methods=['POST'])
def check_user():
    user_data = request.json
    # temp_password = user_data['password']
    # salt = bcrypt.gensalt(prefix=b"md5")
    print(user_data)
    email = user_data["email"]
    password = user_data["password"]

    u = db.session.query(User).where(User.email == email).first()
    print(u.password == password, u.email, u.password, password)
    if u == None or (not u.password == password):
        return jsonify({"success": False}), 400

    return jsonify({"success": True})


# Create
@app.route('/signup', methods=['POST'])
def create_user():
    user_data = request.json
    # temp_password = user_data['password']
    # salt = bcrypt.gensalt(prefix=b"md5")
    try:
        email = user_data['email']
        password = user_data['password']
        print(email, password)
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"success": True})

    except Exception as e:
        print(e)
        return jsonify({"success": False}), 400


# Read
@app.route('/getusers', methods=['GET'])
def getUsers():
    all_users = []
    users = User.query.all()
    for user in users:
        results = {
            "name": user.name,
            "email": user.email,
        }
        all_users.append(results)
    return jsonify({
        "status": True,
        "users": all_users,
        "total_users": len(users),
    })


# Update
@app.route("/users/<string:email>", methods=['PATCH'])
def update_user(email):
    user = User.query.get(email)
    name = request.json['name']
    image = request.json['image']

    if user is None:
        abort(404)
    else:
        user.name = name
        user.image = image
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": "Updated"})


# Delete
@app.route("/users/<string:email>", methods=['DELETE'])
def delete_user(email):
    user = User.query.get(email)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"status": "Deleted"})

@app.route('/addsensors', methods=['POST'])
def create_user():
    sensor_data = request.json
    # temp_password = user_data['password']
    # salt = bcrypt.gensalt(prefix=b"md5")
    try:
        sensor_name = sensor_data['sensor_name']
        location = sensor_data['location']
        pin = sensor_data['pin']
        status = sensor_data['status']
        print(sensor_name, location)
        sensor = Sensor(sensor_name=sensor_name, location=location, pin=pin, status=status)
        db.session.add(sensor)
        db.session.commit()

        return jsonify({"success": True})

    except Exception as e:
        print(e)
        return jsonify({"success": False}), 400

@app.route('/getsensors', methods=['GET'])
def getSensors():
    try:
        all_sensors = []
        sensors = Sensor.query.all()
        for sensor in sensors:
            results = {
                "sensor_name": sensor.sensor_name,
                "location": sensor.location,
                "pin": sensor.pin,
                "status": sensor.status
            }
            all_sensors.append(results)
        return jsonify({
            "status": True,
            "sensors": all_sensors,
            "total_sensors": len(sensors),
        })
    except Exception as e:
        print(e)
        return jsonify({}), 400

@app.route("/sensors/<int:pin>", methods=['PATCH'])
def update_sensor(pin):
    sensor = Sensor.query.get(pin)
    sensor_name = request.json['sensor_name']
    location = request.json['location']

    if sensor is None:
        abort(404)
    else:
        sensor.sensor_name = sensor_name
        sensor.location = location
        db.session.add(sensor)
        db.session.commit()
        return jsonify({"status": "Updated"})


if __name__ == '__main__':
    app.run(port=5000, debug=True)

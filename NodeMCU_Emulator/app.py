from flask import Flask, request as req, jsonify

from flask_cors import CORS
from itsdangerous import json

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def changestatus():
    try:
        for i in req.args.items():
            print(i)
        return jsonify({"Success": True})
    except:
        return jsonify({"Success": False})
    

if __name__ == "__main__":
    app.run(port=2000, debug=True)
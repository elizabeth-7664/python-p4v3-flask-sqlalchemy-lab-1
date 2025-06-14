#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return jsonify({"message": "Flask SQLAlchemy Lab 1"}), 200

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return jsonify(earthquake.to_dict()), 200
    return jsonify({"message": f"Earthquake {id} not found."}), 404

@app.route('/earthquakes/magnitude/<float:mag>', methods=['GET'])
def get_earthquakes_by_magnitude(mag):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= mag).all()
    return jsonify({
        "count": len(earthquakes),
        "earthquakes": [eq.to_dict() for eq in earthquakes]
    }), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)

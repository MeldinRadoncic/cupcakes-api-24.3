"""Flask app for Cupcakes"""


import json
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0258@localhost:5432/cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

# Render form on home page
@app.route('/')
def home_page():
    return render_template('index.html')


# Get list of all Cupcakes
@app.route('/api/cupcakes')
def list_cupcakes():
    all_cupcakes= [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


# Get info of single cupcake base on cupcake id
@app.route('/api/cupcakes/<int:cupcake_id>')
def single_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

# Create a new Cupcake
@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    new_cupcake = Cupcake(flavor=request.json['flavor'],size=request.json['size'],
     rating=request.json['rating'] , image=request.json['image'])
    db.session.add(new_cupcake)
    db.session.commit()
    res = jsonify(new_cupcake.serialize())
    return (res,201)

# Update single cupcake
@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    # if input left it blank then cupcake holds the same value like before
    cupcake.flavor=request.json.get('flavor', cupcake.flavor)
    cupcake.size=request.json.get('size', cupcake.size)
    cupcake.rating=request.json.get('rating', cupcake.rating)
    cupcake.image=request.json.get('image', cupcake.image)
    
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

"""Flask app for Cupcakes"""
import os

from flask import Flask, jsonify, request, render_template
from models import db, Cupcake, connect_db, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get("/")
def homepage():
    """Displays homepage"""
    return render_template("index.html")


@app.get("/api/cupcakes")
def get_cupcakes_data():
    """
    Get info about all cupcakes.
    Returns JSON {'cupcakes': [{
        id, flavor, size, rating, image_url
    }, ...]}"""

    cupcakes_data = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes_data]
    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def get_single_cupcake_data(cupcake_id):
    """
    Get info about a single cupcake.
    Returns JSON {cupcake: {id, flavor, size, rating, image_url}}"""

    cupcake_data = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=cupcake_data.serialize())


@app.post("/api/cupcakes")
def add_cupcake():
    """
    Create new cupcake and add to db.
    Returns JSON {cupcake: {id, flavor, size, rating, image_url}}"""

    new_cupcake = Cupcake(
        flavor=request.json["flavor"],
        size = request.json["size"],
        rating = request.json["rating"],
        image_url = request.json["image_url"]
        )

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)


@app.patch("/api/cupcakes/<int:cupcake_id>")
def update_single_cupcake(cupcake_id):
    """
    Update existing cupcake.
    Can send JSON {flavor, size, rating, image_url}, each field is optional.
    Returns JSON {cupcake: {id, flavor, size, rating, image_url}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)

    image_url = request.json.get("image_url", cupcake.image_url).strip()
    if not image_url:
        cupcake.image_url = DEFAULT_IMAGE_URL
    else:
        cupcake.image_url = image_url

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_single_cupcake(cupcake_id):
    """
    Remove a cupcake from the db.
    Returns JSON {deleted: [cupcake-id]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(deleted=cupcake_id)

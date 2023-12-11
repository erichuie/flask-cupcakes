"""Flask app for Cupcakes"""
import os

from flask import Flask, render_template, redirect, jsonify, flash, request
from models import db, Cupcake, connect_db

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get("/api/cupcakes")
def get_cupcakes_data():
    """Return JSON {'cupcakes': [{
        id, flavor, size, rating, image_url
    }]}"""

    cupcakes_data = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes_data]
    return jsonify(cupcakes=serialized)
from flask import Flask, jsonify, request
from pymongo import MongoClient
from extensions.extensions import mongo
from flask_cors import CORS

app = Flask (__name__)
app.config ['MONGO_URI'] = 'mongodb+srv://admin:123@cluster0.95hrdhh.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(app.config['MONGO_URI'])
db = client['itemFoodDb']
mongo.init_app(app)
from flask_pymongo import pymongo
import os

client = pymongo.MongoClient(os.environ.get('MONGODB_URI')) 
db = client.get_database('playcrate')
games = db.games
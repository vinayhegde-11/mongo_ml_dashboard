from pymongo import MongoClient
from bson import ObjectId
from config_loader import load_config

config = load_config('config.yml')
# MongoDB connection (replace with your MongoDB connection URI)
client = MongoClient(config['mongodb_url'])  # Replace with your URI
db = client["mydatabase"]  # Replace with your database name
collection = db["mycollection"]  # Replace with your collection name

def insert_db(output):
    global collection
    ids = []
    for result in output:
        # Insert the data into MongoDB
        inserted_id = collection.insert_one(result).inserted_id
        # Confirmation message
        print(f"Data inserted with ID: {inserted_id}")
        ids.append(inserted_id)
    return ids

def get_image_path(mongo_id):
    # Connect to the MongoDB server
    global client, db, collection
    # Convert the string id to ObjectId
    object_id_str = mongo_id.get('id')
    if object_id_str is None:
        raise ValueError("The input dictionary must contain an 'id' key.")
    
    object_id = ObjectId(object_id_str)  # Convert to ObjectId
    # Query the database for the document with the specified ObjectId
    document = collection.find_one({'_id': object_id})
    if document:
        # Retrieve the image_path
        return document.get('image_path')  # Adjust this key if your field is named differently
    else:
        return None  # Document not found


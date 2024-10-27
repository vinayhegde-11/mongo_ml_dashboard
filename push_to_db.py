from pymongo import MongoClient

# MongoDB connection (replace with your MongoDB connection URI)
client = MongoClient("mongodb://localhost:27017/")  # Replace with your URI
db = client["mydatabase"]  # Replace with your database name
collection = db["mycollection"]  # Replace with your collection name

def insert_db(output):
    ids = []
    for result in output:
        # Insert the data into MongoDB
        inserted_id = collection.insert_one(result).inserted_id
        # Confirmation message
        print(f"Data inserted with ID: {inserted_id}")
        ids.append(inserted_id)
    return ids


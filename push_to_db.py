# org_images/2024-10-22/2024-10-22_204215.jpg

from pymongo import MongoClient

# MongoDB connection (replace with your MongoDB connection URI)
client = MongoClient("mongodb://localhost:27017/")  # Replace with your URI
db = client["mydatabase"]  # Replace with your database name
collection = db["mycollection"]  # Replace with your collection name

# Example output data to be inserted into MongoDB
output = {
    "image_path": "/home/hegde/project/image_detect_upload/org_images/2024-10-22/hrse.jpg",
    "class_name": "newhrse",
    "time": "2024-10-22 20:59:23"
}

# Insert the data into MongoDB
inserted_id = collection.insert_one(output).inserted_id

# Confirmation message
print(f"Data inserted with ID: {inserted_id}")

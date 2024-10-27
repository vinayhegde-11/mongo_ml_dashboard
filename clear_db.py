from pymongo import MongoClient


def delete_db():
    # MongoDB connection (replace with your MongoDB connection URI)
    client = MongoClient("mongodb://localhost:27017/")  # Replace with your URI
    # Specify the name of the database you want to delete
    database_name = "mydatabase"  # Replace with your database name
    # Delete the database
    client.drop_database(database_name)
    print(f"Database '{database_name}' has been deleted.")


def clear_db():
    # MongoDB connection (replace with your MongoDB connection URI)
    client = MongoClient("mongodb://localhost:27017/")  # Replace with your URI
    db = client["mydatabase"]  # Replace with your database name
    collection = db["mycollection"]  # Replace with your collection name
    # Clear the collection
    result = collection.delete_many({})  # This will delete all documents in the collection
    print(f"Cleared {result.deleted_count} documents from the collection.")

if __name__ == "__main__":
    clear_db()
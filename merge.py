import streamlit as st
import pika
from bson import ObjectId
import json
from datetime import datetime
from pymongo import MongoClient
from PIL import Image
from push_to_db import insert_db
from read_and_save import read_and_save_input_image
from read_rabbitmq import read_from_rabbitmq
from s3_upload import upload_to_s3
from detect import detect
from process_output import post_process
from config_loader import load_config
import io
import base64
import time
import os

config = load_config('config.yml')
# MongoDB connection (replace with your MongoDB connection URI)
client = MongoClient(config['mongodb_url'])  # Replace with your URI
db = client["mydatabase"]  # Replace with your database name
collection = db["mycollection"]  # Replace with your collection name

# Function to fetch data from MongoDB
def fetch_data():
    # Fetch the latest 10 documents from MongoDB collection, sorted by time descending
    data = list(collection.find().sort("time", -1).limit(10))
    return data


# Function to filter data based on class_name and date
def filter_data(data, selected_class, selected_date):
    if selected_class != "All":
        data = [d for d in data if d["class_name"] == selected_class]
    if selected_date != "All":
        data = [d for d in data if d["time"].startswith(selected_date)]
    return data

# Function to get distinct dates in YYYY-MM-DD format
def get_distinct_dates():
    raw_dates = collection.distinct("time")
    formatted_dates = sorted({date.split(" ")[0] for date in raw_dates})
    return ["All"] + formatted_dates
def portal_page():
    st.title("Dashboard")

    # Create a container for the filters at the top
    filter_col1, filter_col2 = st.columns([3, 1])  # Wider column for class filter, narrower for date filter

    with filter_col1:
        all_classes = ["All"] + list(collection.distinct("class_name"))  # Get distinct class names
        selected_class = st.selectbox("Filter by Class", all_classes)

    with filter_col2:
        all_dates = get_distinct_dates()  # Get formatted distinct dates
        selected_date = st.selectbox("Filter by Date", all_dates)

    # Add an empty line for spacing
    st.write("")  

    # Create a section for displaying data
    data_placeholder = st.empty()

    # Clear previous entries and avoid duplicate/shadow entries
    with data_placeholder.container():
        # Fetch data from MongoDB
        data = fetch_data()

        # Filter data based on user selections
        filtered_data = filter_data(data, selected_class, selected_date)
        
        if filtered_data:
            # Display header row for the data table
            header_col1, header_col2, header_col3, header_col4 = st.columns([2, 1, 1, 1])
            header_col1.write("**Image**")
            header_col2.write("**Class**")
            header_col3.write("**Count**")  # Add count header
            header_col4.write("**Date**")

            # Display data rows
            for entry in filtered_data:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])  # Added a column for count

                # Image display (handle missing or incorrect image path)
                img_path = entry.get("image_path")
                if img_path and os.path.exists(img_path):  # Ensure the image file exists
                    try:
                        # Load image using the image path
                        img = Image.open(img_path)

                        # Create a copy of the original image and resize it to 60x60 pixels for inline display
                        img_64 = img.copy().resize((60, 60))

                        # Convert the resized image to bytes for inline display
                        img_bytes = io.BytesIO()
                        img_64.save(img_bytes, format='PNG')
                        img_base64 = base64.b64encode(img_bytes.getvalue()).decode()

                        # Use file:/// protocol to open the original image
                        file_path = f"file://{img_path}"  # Adjusted to use file:/// protocol
                        col1.markdown(f'<a href="{file_path}" target="_blank"><img src="data:image/png;base64,{img_base64}" style="width:60px;height:60px;"></a>', unsafe_allow_html=True)

                    except Exception as e:
                        continue  # Skip this entry if the image can't be loaded
                else:
                    col1.write("No Image")  # Placeholder if image_path is not available
                
                # Class display
                col2.write(entry['class_name'])  # Directly show the class name

                # Class count display
                col3.write(entry.get('count', 'N/A'))  # Display class count from MongoDB entry
                
                # Split the time into date and time
                date_time = entry['time'].split(" ")
                date_part = date_time[0] if len(date_time) > 0 else ""
                time_part = date_time[1] if len(date_time) > 1 else ""

                # Display date and time in separate lines
                col4.write(date_part)  # Display date
                col4.write(time_part)  # Display time

                # Draw a horizontal line to separate entries
                st.markdown("---")
        else:
            st.write("No data found for the selected filters.")
        
        time.sleep(10)

# Function to push image path to RabbitMQ
def push_to_rabbitmq(data):
    try:
        rmq_user = config["rmq_user"]
        rmq_pass = config["rmq_pass"]
        rmq_topic = config["rmq_topic"]
        rmq_host = config["rmq_host"]
        rmq_vhost = config["rmq_vhost"]

        credentials = pika.PlainCredentials(rmq_user, rmq_pass)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_host, virtual_host=rmq_vhost, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=rmq_topic, durable=True)
        if 'id' in data:
            for object_id in data['id']:
                # Convert to JSON
                message = json.dumps({'id': object_id})
                channel.basic_publish(exchange='', routing_key=rmq_topic, body=message, properties=pika.BasicProperties(delivery_mode=2))
                print(f" [x] Sent '{message}' to queue '{rmq_topic}'")
    except Exception as e:
        print(f"An error occurred while pushing to RabbitMQ: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

def serialize_data(data):
    if isinstance(data, dict):
        return {k: serialize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)  # Convert ObjectId to string
    else:
        return data

# Function for the image upload page
def upload_page():
    st.title("Image Upload Example")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image_path = read_and_save_input_image(uploaded_file)
        final = []
        detections = detect(image_path)
        count_class = post_process(detections)
        for item in count_class:
            cls_dict = {
                "image_path": image_path,
                "class_name": item[0],
                "count": item[1],
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            final.append(cls_dict)
        
        ids = insert_db(final)
        print(ids)
        push_to_rabbitmq(serialize_data({"id": ids}))
        read_from_rabbitmq()

        # st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

# Main function to manage the app
# def main():
#     st.sidebar.title("Navigation")
#     app_mode = st.sidebar.selectbox("Choose a page", ["Upload", "Dashboard"])

#     if app_mode == "Upload":
#         upload_page()
#     elif app_mode == "Dashboard":
#         portal_page()

# if __name__ == "__main__":
#     main()
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["Dashboard", "Upload Image"])

    # Create a container for page content
    with st.container():
        if page == "Dashboard":
            st.empty()
            portal_page()  # Call the portal page function
            st.empty()
        elif page == "Upload Image":
            st.empty()
            upload_page()  # Call the upload page function
            st.empty()

if __name__ == "__main__":
    main()

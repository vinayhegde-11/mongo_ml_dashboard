import streamlit as st
from pymongo import MongoClient
from PIL import Image
import io
import base64
import time
import os

# MongoDB connection (replace with your MongoDB connection URI)
client = MongoClient("mongodb://localhost:27017/")  # Replace with your URI
db = client["mydatabase"]  # Replace with your database name
collection = db["mycollection"]  # Replace with your collection name

# Function to fetch data from MongoDB
def fetch_data():
    # Fetch all documents from MongoDB collection
    data = list(collection.find())
    return data

# Function to filter data based on class_name and date
def filter_data(data, selected_class, selected_date):
    # Filter by class_name
    if selected_class != "All":
        data = [d for d in data if d["class_name"] == selected_class]
    
    # Filter by date (only the date part)
    if selected_date != "All":
        data = [d for d in data if d["time"].startswith(selected_date)]
    
    return data

# Function to get distinct dates in YYYY-MM-DD format
def get_distinct_dates():
    # Retrieve distinct dates and format them
    raw_dates = collection.distinct("time")
    formatted_dates = sorted({date.split(" ")[0] for date in raw_dates})  # Keep only the date part
    return ["All"] + formatted_dates  # Add "All" option

# Page layout
st.title("MongoDB Data Dashboard")

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

# Keep the app refreshing every 10 seconds
while True:
    # Clear previous entries and avoid duplicate/shadow entries
    with data_placeholder.container():
        # Fetch data from MongoDB
        data = fetch_data()

        # Filter data based on user selections
        filtered_data = filter_data(data, selected_class, selected_date)
        
        if filtered_data:
            # Display header row for the data table
            header_col1, header_col2, header_col3 = st.columns([2, 1, 1])
            header_col1.write("**Image**")
            header_col2.write("**Class**")
            header_col3.write("**Date**")

            # Display data rows
            for entry in filtered_data:
                col1, col2, col3 = st.columns([2, 1, 1])

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
                
                # Split the time into date and time
                date_time = entry['time'].split(" ")
                date_part = date_time[0] if len(date_time) > 0 else ""
                time_part = date_time[1] if len(date_time) > 1 else ""

                # Display date and time in separate lines
                col3.write(date_part)  # Display date
                col3.write(time_part)  # Display time

                # Draw a horizontal line to separate entries
                st.markdown("---")
        else:
            st.write("No data found for the selected filters.")
    
    # Auto-refresh every 10 seconds
    time.sleep(10)

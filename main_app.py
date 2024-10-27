import streamlit as st
import pika
from datetime import datetime
import json
from read_and_save import read_and_save_input_image
from detect import detect
from push_to_db import insert_db
from process_output import post_process

# Function to push image path to RabbitMQ
def push_to_rabbitmq(data):
    try:
        rabbitmq_host = 'localhost'  # Change if RabbitMQ is running on a different host
        queue_name = 'image_path'   # The name of the queue
        vhost = "entries"

        # Connect to RabbitMQ server
        credentials = pika.PlainCredentials('vinay', 'vinay')  # Use the created user and password
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, virtual_host=vhost, credentials=credentials))
        channel = connection.channel()

        # Declare a queue (create it if it doesn't exist)
        channel.queue_declare(queue=queue_name, durable=True)

        # Convert the dictionary to a JSON string
        message_str = json.dumps(data)

        # Publish image path to the queue
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message_str,  # Send the JSON string
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

        print(f" [x] Sent '{message_str}' to queue '{queue_name}'")

    except Exception as e:
        print(f"An error occurred while pushing to RabbitMQ: {e}")

    finally:
        # Close the connection
        if 'connection' in locals() and connection.is_open:
            connection.close()

# Title of the Streamlit app
st.title("Image Upload Example")

# Create an image uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Read and save the input image
    image_path = read_and_save_input_image(uploaded_file)
    final = []
    detections = detect(image_path)
    count_class = post_process(detections)
    for item in count_class:
        cls_dict = {
            "image_path": image_path,
            "class_name": item[0],
            "count": item[1],
            "time": datetime.now().strftime("%Y-%m-%d_%H%M%S")
        }
        final.append(cls_dict)
    
    ids = insert_db(final)

    # # Push the image path to RabbitMQ
    # push_to_rabbitmq(output)

    # Optionally display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

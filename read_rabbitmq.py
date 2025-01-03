import pika
import json
import time
from push_to_db import get_image_path
from s3_upload import upload_to_s3
from config_loader import load_config
config = load_config('config.yml')

def read_from_rabbitmq():
    try:
        # Callback to process messages and push to another queue
        def callback(ch, method, properties, body):
            message = json.loads(body)
            org_image_path = get_image_path(message)
            s3_res = upload_to_s3(org_image_path)
            if s3_res is not None:
                print(f"uploaded image > {s3_res}")
            else:
                print("Error uploading")
            
            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # AMQP connection details (use amqp://user:password@host:port/vhost)
        amqp_url = config['rabbitmq_url']

        # Combined URL parameters and connection
        connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
        channel = connection.channel()

        # Declare both the original and target queues
        channel.queue_declare(queue='image_path', durable=True)

        # Start consuming from the original queue
        channel.basic_consume(queue='image_path', on_message_callback=callback)

        print("Waiting for messages. To exit, press CTRL+C.")
        channel.start_consuming()
    except Exception as e:
        print(f"An error occurred while reading from RabbitMQ: {e}")

    finally:
        # Close the connection (this will not be reached unless you stop consuming)
        if 'connection' in locals() and connection.is_open:
            connection.close()



# Example of using the function
if __name__ == "__main__":
    read_from_rabbitmq()

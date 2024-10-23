import pika
import json
import time

# Function to process and print the message
def process_message(data):
    print(f"Processing Message: {data}")


def read_from_rabbitmq():
    try:
        # Callback to process messages and push to another queue
        def callback(ch, method, properties, body):
            message = json.loads(body)
            process_message(message)
            
            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
            # Push the message to another queue (e.g., 'processed_queue')
            # channel.basic_publish(
            #     exchange='',
            #     routing_key='processed_queue',
            #     body=json.dumps(message),
            #     properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
            # )
            # print(f"Message re-published to 'processed_queue'.")

        # AMQP connection details (use amqp://user:password@host:port/vhost)
        amqp_url = 'amqp://vinay:vinay@localhost:5672/entries'

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

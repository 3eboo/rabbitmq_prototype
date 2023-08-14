import csv
import json
import random
import time

import pika


def produce_message(filepath: str):
    time.sleep(20)  # waiting for the instance to fully provision.
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('myrabbit', virtual_host='my_vhost',
                                      credentials=pika.PlainCredentials('user', 'pass')))
        channel = connection.channel()
    except pika.exceptions.AMQPConnectionError as e:
        raise RuntimeError(f"Error connecting to RabbitMQ: {e}")

    exchange_name = 'edits'
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            message = json.dumps(row)
            channel.basic_publish(exchange=exchange_name, routing_key='', body=message)
            time.sleep(random.uniform(0, 1))

    channel.basic_publish(exchange=exchange_name, routing_key='', body=b'END')
    connection.close()


if __name__ == '__main__':
    file_path = 'sample_data.csv'
    produce_message(file_path)
    print("Messages produced successfully.")

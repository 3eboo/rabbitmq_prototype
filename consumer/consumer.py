import json
import time

import pika


class EditCounter:
    def __init__(self):
        self.global_edits: int = 0
        self.german_wiki_edits: int = 0
        self.start_time: float = time.time()
        self.data_results: list = []

    def process_message(self, body: bytes):
        data = json.loads(body)
        if data['type'] == 'edit':
            self.global_edits += 1
            if data['server_name'] == 'de.wikipedia.org':
                self.german_wiki_edits += 1
        elapsed_time_in_min = (time.time() - self.start_time) / 60

        global_edits_per_min = calculate_target_per_minute(self.global_edits, elapsed_time_in_min)
        german_edits_per_min = calculate_target_per_minute(self.german_wiki_edits, elapsed_time_in_min)

        self.data_results.append({
            'elapsed_time': elapsed_time_in_min,
            'global_edits_per_min': round(global_edits_per_min, 2),
            'german_edits_per_min': round(german_edits_per_min, 2)
        })
        print(f"Global edits per minute: {global_edits_per_min:.2f}")
        print(f"German edits per minute: {german_edits_per_min:.2f}")

    def save_data(self):
        with open('results.json', 'w') as json_file:
            json.dump(self.data_results, json_file)


def calculate_target_per_minute(target: int, elapsed_time: float) -> float:
    return target / elapsed_time


def callback(ch, method, properties, body: bytes):
    if body != b'END':
        edit_counter.process_message(body)
    else:
        edit_counter.save_data()


if __name__ == '__main__':
    time.sleep(30)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('myrabbit', virtual_host='my_vhost',
                                  credentials=pika.PlainCredentials('user', 'pass')))
    channel = connection.channel()

    exchange_name = 'edits'
    queue_name = 'edits_queue'

    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
    channel.queue_declare(queue=queue_name)

    channel.queue_bind(queue_name, exchange_name, routing_key='')  # bind queue with exchange used to send messages.

    edit_counter = EditCounter()

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print('Consumer is waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

from confluent_kafka import Consumer

import os

if __name__ == '__main__':
    config = {
        'bootstrap.servers': os.getenv('KAFKA_HOSTS'),
        'group.id': 'escort-book-statistics-consumer',
        'enable.auto.commit': True,
        'auto.offset.reset': 'earliest',
    }
    consumer = Consumer(config)
    consumer.subscribe(['test-topic'])

    try:
        while True:
            message = consumer.poll(1.0)
            if message is None:
                continue
            elif message.error():
                print(f'Error receiving the message {message.error()}')
            else:
                print('Processed message')
                print(message.value().decode('utf-8'))
    except KeyboardInterrupt:
        print('Gracefully stop the consumer')
    finally:
        consumer.close()

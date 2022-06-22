import os
import json

from confluent_kafka import Consumer

from services.strategy_manager import initialize_manager


async def listen() -> None:
    config = {
        'bootstrap.servers': os.getenv('KAFKA_HOSTS'),
        'group.id': 'escort-book-statistics-consumer',
        'enable.auto.commit': True,
        'auto.offset.reset': 'earliest',
    }
    consumer = Consumer(config)
    consumer.subscribe(['operations-statistics'])

    try:
        while True:
            message = consumer.poll(1.0)
            if message is None:
                continue
            elif message.error():
                print(f'Error receiving the message {message.error()}')
            else:
                parsed_message: dict = json.loads(message.value().decode('utf-8'))
                await initialize_manager(parsed_message['operation']).process_message(parsed_message)
                print('Processed message')
    except KeyboardInterrupt:
        print('Gracefully stop the consumer')
    finally:
        consumer.close()

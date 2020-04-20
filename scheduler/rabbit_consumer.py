import config
import pika, logging, time, json

logger = logging.getLogger('test_client.py')

# credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PW)
# parameters = pika.ConnectionParameters(host=config.RABBITMQ_HOST, port=config.RABBITMQ_PORT, credentials=credentials)
parameters = pika.ConnectionParameters(host=config.RABBITMQ_HOST, port=config.RABBITMQ_PORT)
rabbitmq_connection = pika.BlockingConnection(parameters)
channel = rabbitmq_connection.channel()

channel.queue_declare(queue=config.RABBITMQ_QUEUE, durable=True)
logger.debug(f'consumer ready. Waiting for messages.')


def callback(ch, method, properties, body):
    # time.sleep(0.5)
    print(f'{ch} {method} {properties} {json.loads(body)}')
    logger.info(f'msg data: {json.loads(body)} and send back delivery_tag={method.delivery_tag}')
    ch.basic_ack(delivery_tag=method.delivery_tag)



if __name__ == "__main__":
    try:
        channel.basic_qos(prefetch_count=10)
        channel.basic_consume(queue=config.RABBITMQ_QUEUE, on_message_callback=callback)

        channel.start_consuming()
    except Exception as e:
        logger.exception(f'closed test client rabbitmq consumer exception:{e}')
        rabbitmq_connection.close()

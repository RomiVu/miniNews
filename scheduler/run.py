#!/usr/bin/env python
import config

import json, logging
import pika
from pymongo import MongoClient
from twisted.internet import reactor, task

from schedule import Scheduler

logger = logging.getLogger('run.py')

try:
    mongo_client = MongoClient(config.MONGO_HOST, config.MONGO_PORT)
    collection = mongo_client[config.MONGO_DB_NAME][config.MONGO_DB_COL_NAME]
except Exception as e:
    logger.error(f'mongodb client failed args:{config.MONGO_HOST}:{config.MONGO_PORT}. exception_info:{e}')
    raise("MongoDB can't connected")

try:    
    # credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PW)
    # parameters = pika.ConnectionParameters(host=config.RABBITMQ_HOST, port=config.RABBITMQ_PORT, credentials=credentials)
    parameters = pika.ConnectionParameters(host=config.RABBITMQ_HOST, port=config.RABBITMQ_PORT)
    rabbitmq_connection = pika.BlockingConnection(parameters)
    channel = rabbitmq_connection.channel()

    channel.queue_declare(queue=config.RABBITMQ_QUEUE, durable=True)
except Exception as e:
    logger.error(f'rabbitmq client failed args:{config.RABBITMQ_HOST}:{config.RABBITMQ_PORT}. exception_info:{e}')
    raise("rabbitmq can't connected")


def mq_sender(data):
    logger.info(f'tasks pulished! data:{data}')
    channel.basic_publish(
        exchange='',
        routing_key=config.RABBITMQ_QUEUE,
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=config.RABBITMQ_DURABLE_MODE,  # make message persistent
    ))
# to do list:
#    fixed time schedule
#    schedule request mongodb
#    pymongo document data format
#    pymongo, rabitmq, python docker deploy
EXISTED = set()

def scan_data_base():
    EXISTED.clear()
    logging.info(f'Befor query: EXISETED {len(EXISTED)}')
    for task in collection.find():
        interval  = task.get('interval', None)
        priority = task.get('priority', 10)
        body_dict = task.get('data', None)
        url = body_dict['url']
        EXISTED.add(url)
    logging.info(f'after query: EXISETED {len(EXISTED)}')
        

def cbLoopDone(result):
    logging.info("Loop done.")
    reactor.stop()


def ebLoopFailed(failure):
    logging.error(failure.getBriefTraceback())
    reactor.stop()


if __name__ == "__main__":
    loop = task.LoopingCall(scan_data_base)
    loopDeferred = loop.start(1800.0)
    loopDeferred.addCallback(cbLoopDone)
    loopDeferred.addErrback(ebLoopFailed)

    reactor.run()

    # try:
    #     s = Scheduler()
    #     for task in collection.find():
    #         interval  = task.get('interval', None)
    #         priority = task.get('priority', 10)
    #         body_dict = task.get('data', None)
    #         if interval is None or body_dict is None:
    #             logger.warning(f'incomplete tasks msg interval:{interval}, priority:{priority}, data:{body_dict}')
    #             continue
    #         logger.info(f'tasks added! interval:{interval}, priority:{priority}, data:{body_dict}')
    #         s.add_into_queue(interval, priority, mq_sender, body_dict)

    #     s.run()
    # except Exception as e:
    #     logger.exception(f'run.py terminated due to {e}')
    #     rabbitmq_connection.close()
    #     mongo_client.close()
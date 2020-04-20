import json

from scrapy import Spider, Request

import config
from connection import channel

class RabbitmqSpider(Spider):
    
    def start_requests(self):
        def mq_call_back(channel, method, properties, body):
            data = json.loads(body)
            yield Request(data['url'], dont_filter=True)
        channel.basic_get(config.RABBITMQ_QUEUE, callback=mq_call_back)
from scrapy import Spider, Request
import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()


class RabbitmqSpider(Spider):
    name = 'exampla'
    
    def start_requests(self):           
        _, _, body = channel.basic_get('task_queue')
        data = json.loads(body)
        print(f'--------- {data}')
        yield Request(data['url'], dont_filter=True)
# miniNews

1. React + Flask + Mongo/Mysql
    -- database visualization and CRUD API
2. React + Tornado + ES
   -- ElasticSearch query/filter/search
3. scheduler
   -- publish task into Redis queue from Mongodb regularly
4. Redis Queue
   -- duplicate_db /  request_queue / start_queue
5. Scrapy workers
   -- one subscribed from start_queue
      others subscribed from request_queue
      both connected to duplicate_db
      publish items into Kafka
6. Kafka Queue
   -- receive items and give it to data cleaning and saving
7. NLP worker
   -- consumen Kafka queue and process it, then save it into ES
8. ElasticSearch
   -- final data
---

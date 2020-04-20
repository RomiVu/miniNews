import logging, os

# from dotenv import load_dotenv


# # load '.env' file into os.env
# load_dotenv()


MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'tasks')
MONGO_DB_COL_NAME = os.getenv('MONGO_DB_COL_NAME', 'test-tasks')

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'localhost')
RABBITMQ_PW = os.getenv('RABBITMQ_PW', 'localhost')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'task_queue')
RABBITMQ_DURABLE_MODE  = int(os.getenv('RABBITMQ_DURABLE_MODE', 2))

LOGGING_PATH = os.getenv('LOGGING_PATH', '.')
LOGGING_FILENAME = os.getenv('LOGGING_FILENAME', 'test.log')
LOGGING_DEFAULT_LEVEL = os.getenv('LOGGING_DEFAULT_LEVEL', 'INFO')
LOGGING_DEFAULT_FORMAT = os.getenv('LOGGING_DEFAULT_FORMAT','%(asctime)s, %(filename)s, %(levelname)s, %(message)s')

'''    
'CRITICAL': CRITICAL,
'FATAL': FATAL,
'ERROR': ERROR,
'WARN': WARNING,
'WARNING': WARNING,
'INFO': INFO,
'DEBUG': DEBUG,
'NOTSET': NOTSET,
'''

logging.basicConfig(level=LOGGING_DEFAULT_LEVEL, format='%(asctime)s, %(filename)s, %(levelname)s, %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=os.path.join(LOGGING_PATH, LOGGING_FILENAME),
                    filemode='a')
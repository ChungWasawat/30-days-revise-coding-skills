import requests
import logging
import time
from pythonjsonlogger import jsonlogger


logger = logging.getLogger(__name__)
logger.info("Server started")

# basic config for learning
# Set this in your main config (INFO or DEBUG) -not DEBUG as it will flood disk
logging.basicConfig(level=logging.INFO)

# flexible for production
LOGGING_DATA = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter', # Custom formatter
            'format': '%(timestamp)s %(levelname)s %(message)s'
        }
    },
    # tell python where to send data
    'handlers': {  
        # print on terminal                                         
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
        },
        # print on file
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            # choose which format
            'formatter': 'detailed',
            'filename': 'errors.log',
            'maxBytes': 10485760, # max is 10MB
            'backupCount': 5,
        },
    },
    'loggers': {
        # safety net to log all things
        '': { # Root logger
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        # set for specific things
        'my_project.database': { # Specific settings for DB module
            'level': 'DEBUG',
            'propagate': False,     # not send anything to root logger
            'handlers': ['console'],
        }
    }
}
#logging.config.dictConfig(LOGGING_DATA)


def fetch_with_retry(url, params, retries=3, wait=2):#
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            print(response.status_code)
            print(response.raise_for_status())
            return response.json()
        except requests.exceptions.Timeout:
            logging.warning(f"Attempt {attempt}: Timeout", exc_info=True)
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error: {e.response.status_code}", exc_info=True)
            break                           # don't retry on 4xx
        except requests.exceptions.ConnectionError:
            logging.warning(f"Attempt {attempt}: Connection error", exc_info=True)
        time.sleep(wait)
    return None                             # all retries exhausted


# check 404
url="https://jsonplaceholder.typicode.com/posts/99999"
print(fetch_with_retry(url, []))


# check timeout
url = "https://httpbin.org/delay/10"
print(fetch_with_retry(url, []))

# check connection
url = "https://this-domain-does-not-exist-xyz.com"
print(fetch_with_retry(url, []))

# check 500
url="https://httpbin.org/status/500"
print(fetch_with_retry(url, []))  




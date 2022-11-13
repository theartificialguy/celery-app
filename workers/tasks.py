from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

celery = Celery('tasks_queue', broker='RabbitMQ')

@celery.task(name='script_one')
def script_one(args):
    logger.info('Got request, starting worker thread...')
    logger.info('args: {}'.format(args))
    '''    
    -> get current stock data from third party api or a data layer.
    -> Do some computation on stock data until the user stops this script 
        from frontend or the script stops itself due to some other reason/condition.
    -> Send push notification to user device if some condition is met.    
    '''
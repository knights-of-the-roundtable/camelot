import http.client as httplib
from log_cfg import logger

def asset_outcomes(event, context):
    logger.debug('event: {}, context: {}'.format(event, context))

    return {
        'statusCode': httplib.OK,
        'body': {
            'outcomes': [
                {
                    'id' : '1',
                    'name' : 'Blue Wins'
                }
            ] 
        }
    }

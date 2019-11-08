import os

from models import Player
from db_util import db_session
from lambda_decorators import ssm_parameter_store, json_http_resp, load_json_body, cors_headers

@ssm_parameter_store('/prod/camelot/db-password')
def lambda_handler(event, context):
    with db_session(os.environ['HOST'], context.parameters['/prod/camelot/db-password']) as session:
        session.query(Player).filter(Player.id == event['player']).delete()
    return {'code': 'success'}

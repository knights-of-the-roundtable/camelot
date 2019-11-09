from models import Player
from db_util import db_session
from lambda_decorators import json_http_resp, load_json_body, cors_headers

def lambda_handler(event, context):
    with db_session() as session:
        session.query(Player).filter(Player.id == event['player']).delete()
    return {'code': 'success'}

import os

from models import Player
from db_util import db_session
from lambda_decorators import json_http_resp, load_json_body, cors_headers

@cors_headers(origin="*")
@json_http_resp
@load_json_body
def lambda_handler(event, context):
    body = {}
    request = event['body']
    with db_session(os.environ['AURORA_CLUSTER_ARN'], os.environ['SECRET_ARN']) as session:
        player = Player(first_name=request['first_name'], last_name=request['last_name'])
        session.add(player)
        session.commit()
        body['player'] = player.id
    return body

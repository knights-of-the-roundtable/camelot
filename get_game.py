import os

from models import Game
from db_util import db_session, as_dict
from lambda_decorators import json_http_resp, load_json_body, cors_headers

@cors_headers(origin="*")
@json_http_resp
def lambda_handler(event, context):
    game = {}
    gameId = event['pathParameters']['gameId']
    with db_session(os.environ['AURORA_CLUSTER_ARN'], os.environ['SECRET_ARN']) as session:
        game = as_dict(session.query(Game).filter(Game.id == gameId).first())
    return game

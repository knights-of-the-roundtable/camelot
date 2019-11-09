from models import Game
from db_util import db_session, as_dict
from lambda_decorators import json_http_resp, load_json_body, cors_headers

@cors_headers(origin="https://uxfabric-e2e.app.intuit.com")
@json_http_resp
def lambda_handler(event, context):
    game = {}
    gameId = event['pathParameters']['gameId']
    with db_session() as session:
        game = as_dict(session.query(Game).filter(Game.id == gameId).first())
    return game

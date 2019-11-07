import os

from models import Game
from db_util import db_session, as_dict
from lambda_decorators import ssm_parameter_store, json_http_resp, load_json_body, cors_headers

@cors_headers(origin="*")
@json_http_resp
@ssm_parameter_store('/prod/camelot/db-password')
def lambda_handler(event, context):
    game = {}
    gameId = event['pathParameters']['gameId']
    with db_session(os.environ['HOST'], context.parameters['/prod/camelot/db-password']) as session:
        game = as_dict(session.query(Game).filter(Game.id == gameId).first())
    return game

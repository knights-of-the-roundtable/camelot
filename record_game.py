import json
import os

from models import Game, GamePlayer, Player
from db_util import db_session
from lambda_decorators import ssm_parameter_store, json_http_resp, load_json_body, cors_headers

@cors_headers(origin="*.intuit.com")
@json_http_resp
@ssm_parameter_store('/prod/camelot/db-password')
@load_json_body
def lambda_handler(event, context):
    body = {}
    request = event['body']
    with db_session(os.environ['HOST'], context.parameters['/prod/camelot/db-password']) as session:
        game = Game(outcome_id=request['outcome'], mvp_id=request['mvp'], lvp_id=request['lvp'])

        for player in request['players']:
            game.game_players.append(GamePlayer(player_id=player['player'], role_id=player['role']))
        session.commit()
        body['game'] = game.id
    return body

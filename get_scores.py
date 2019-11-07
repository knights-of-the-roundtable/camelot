import os

from models import Player, Game
from db_util import db_session, as_dict
from lambda_decorators import ssm_parameter_store, json_http_resp, load_json_body, cors_headers

def add_points(players, player, points):
    if 'score' not in players[player]:
        players[player]['score'] = points
    else:
        players[player]['score'] += points

def add_point(players, player):
    add_points(players, player, 1)

def subtract_point(players, player):
    add_points(players, player, -1)

# Order of decorators matters!
@cors_headers(origin="*.intuit.com")
@json_http_resp
@ssm_parameter_store('/prod/camelot/db-password')
def lambda_handler(event, context):
    body = {}
    with db_session(os.environ['HOST'], context.parameters['/prod/camelot/db-password']) as session:
        players = {player.id:{'id': player.id, 'name': player.full_name()} for player in session.query(Player).all()}
        # Handle points from each game
        for game in session.query(Game).all():
            # Handle MVP and LVP points for this game
            add_point(players, game.mvp_id)
            subtract_point(players, game.lvp_id)
            # Handle all the winners for this game
            for gamePlayer in game.game_players:
                if gamePlayer.role.is_good() == game.outcome.is_good():
                    add_point(players, gamePlayer.player_id)
        body = list(players.values())
    return body

import os

from models import Player, Game
from db_util import db_session, as_dict
from lambda_decorators import json_http_resp, load_json_body, cors_headers
from operator import itemgetter

def add_point(players, player):
    players[player]['score'] += 1

def subtract_point(players, player):
    players[player]['score'] -= 1

def add_mvp(players, player):
    add_point(players, player)
    players[player]['mvp'] += 1

def add_lvp(players, player):
    subtract_point(players, player)
    players[player]['lvp'] += 1

def add_win(players, player):
    add_point(players, player)
    players[player]['win'] += 1

def add_loss(players, player):
    players[player]['loss'] += 1

def update_totals(players, player):
    players[player]['games'] = players[player]['win'] + players[player]['loss']
    players[player]['percentage'] = 0 if players[player]['games'] == 0 else players[player]['win'] / players[player]['games']

# Order of decorators matters!
@cors_headers(origin="https://uxfabric-e2e.app.intuit.com")
@json_http_resp
def lambda_handler(event, context):
    body = {}
    with db_session(os.environ['AURORA_CLUSTER_ARN'], os.environ['SECRET_ARN']) as session:
        # Setup players map, and give each player a starting score of 0 in case they haven't played any games
        players = {player.id:{'id': player.id, 'name': player.full_name(), 'score':0, 'win':0, 'loss':0} for player in session.query(Player).all()}
        # Handle points from each game
        for game in session.query(Game).all():
            # Handle MVP and LVP points for this game
            add_mvp(players, game.mvp_id)
            add_lvp(players, game.lvp_id)
            # Handle all the winners for this game
            for gamePlayer in game.game_players:
                if gamePlayer.role.is_good() == game.outcome.is_good():
                    add_win(players, gamePlayer.player_id)
                else:
                    add_loss(players, gamePlayer.player_id)
                update_totals(players, gamePlayer.player_id)

        body = list(players.values())
        body.sort(key=itemgetter('score'), reverse=True)
    return body

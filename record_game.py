import os
import json

from http import HTTPStatus
from models import Game, GamePlayer, Player, Role
from db_util import db_session
from lambda_decorators import ssm_parameter_store, load_json_body, cors_headers

@cors_headers(origin="*")
@ssm_parameter_store('/prod/camelot/db-password')
@load_json_body
def lambda_handler(event, context):
    body = {}
    request = event['body']

    if len(request['players']) < 5 or len(request['players']) > 10:
        return {'statusCode': HTTPStatus.BAD_REQUEST.value, 'body': json.dumps({'errorDescription': 'Players in game must be 5 to 10 inclusive'})}

    if not unique_players(request['players']):
        return {'statusCode': HTTPStatus.BAD_REQUEST.value, 'body': json.dumps({'errorDescription': 'All players in game must be unique people'})}

    if not mvp_lvp_in_game(request):
        return {'statusCode': HTTPStatus.BAD_REQUEST.value, 'body': json.dumps({'errorDescription': 'MVP and LVP must be players in the game'})}

    with db_session(os.environ['HOST'], context.parameters['/prod/camelot/db-password']) as session:
        if not unique_roles(request['players'], session):
            return {'statusCode': HTTPStatus.BAD_REQUEST.value, 'body': json.dumps({'errorDescription': 'Roles assigned exceed max counts'})}

        game = Game(outcome_id=request['outcome'], mvp_id=request['mvp'], lvp_id=request['lvp'])

        for player in request['players']:
            game.game_players.append(GamePlayer(player_id=player['player'], role_id=player['role']))
            
        session.add(game)
        session.commit()
        body['game'] = game.id
    return {'statusCode': HTTPStatus.OK.value, 'body': json.dumps(body)}

def unique_players(players):
    return len(set([player['player'] for player in players])) == len(players)

def mvp_lvp_in_game(request):
    mvp = request['mvp']
    lvp = request['lvp']
    found_mvp = False
    found_lvp = False

    for player in request['players']:
        if player['player'] is mvp:
            found_mvp = True
        if player['player'] is lvp:
            found_lvp = True

    return found_mvp and found_lvp

TEAM_MAPPING = {
    10: (6,4),
    9: (6,3),
    8: (5,3),
    7: (4,3),
    6: (4,2),
    5: (3,2)
}

def unique_roles(players, session):
    roles = {role.id:role for role in session.query(Role).all()}
    role_counts = {}
    good_team = 0
    bad_team = 0
    for player in players:
        if player['role'] not in role_counts:
            role_counts[player['role']] = 1
        else:
            role_counts[player['role']] += 1

    for role_id, count in role_counts.items():
        role = roles[role_id]
        if role.is_power() and count > 1:
            return False
        if role.is_good():
            good_team += count
        else:
            bad_team += count
    
    (good_count, bad_count) = TEAM_MAPPING[len(players)]
    if good_team != good_count or bad_team != bad_count:
        return False

    return True

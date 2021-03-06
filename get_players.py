import os

from models import Player
from db_util import db_session, as_dict
from lambda_decorators import json_http_resp, load_json_body, cors_headers

@cors_headers(origin="*")
@json_http_resp
def lambda_handler(event, context):
    body = {}
    with db_session(os.environ['AURORA_CLUSTER_ARN'], os.environ['SECRET_ARN']) as session:
        body = [{'id': player.id, 'name': player.full_name()} for player in session.query(Player).all()]
    return body

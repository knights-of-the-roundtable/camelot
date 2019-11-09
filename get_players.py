from models import Player
from db_util import db_session, as_dict
from lambda_decorators import json_http_resp, load_json_body, cors_headers

@cors_headers(origin="https://uxfabric-e2e.app.intuit.com")
@json_http_resp
def lambda_handler(event, context):
    body = {}
    with db_session() as session:
        body = [{'id': player.id, 'name': player.full_name()} for player in session.query(Player).all()]
    return body

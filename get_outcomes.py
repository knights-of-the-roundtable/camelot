import os

from models import Outcome
from db_util import db_session, as_dict
from lambda_decorators import json_http_resp, load_json_body, cors_headers

# Order of decorators matters!
@cors_headers(origin="*")
@json_http_resp
def lambda_handler(event, context):
    body = {}
    with db_session(os.environ['AURORA_CLUSTER_ARN'], os.environ['SECRET_ARN']) as session:
        body = [{'id': outcome.id, 'name': outcome.name} for outcome in session.query(Outcome).all()]
    return body

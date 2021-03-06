import os

import bootstrap_db

from db_util import db_session, as_dict
from lambda_decorators import json_http_resp, load_json_body, cors_headers

def lambda_handler(event, context):
    bootstrap_db.bootstrap(os.environ['AURORA_CLUSTER_ARN'], os.environ['SECRET_ARN'])
    return {'code': 'success'}

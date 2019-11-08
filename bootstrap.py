import os
import bootstrap_db

from db_util import db_session, as_dict
from lambda_decorators import ssm_parameter_store, json_http_resp, load_json_body, cors_headers

@ssm_parameter_store('/prod/camelot/db-password')
def lambda_handler(event, context):
    bootstrap_db.bootstrap(os.environ['HOST'], context.parameters['/prod/camelot/db-password'])
    return {'code': 'success'}

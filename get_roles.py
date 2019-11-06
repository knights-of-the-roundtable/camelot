import os

from models import Role
from db_util import db_session, as_dict
from lambda_decorators import ssm_parameter_store, json_http_resp, load_json_body, cors_headers

# Order of decorators matters!
@cors_headers(origin="*.intuit.com")
@json_http_resp
@ssm_parameter_store('/prod/camelot/db-password')
def lambda_handler(event, context):
    body = {}
    with db_session(os.environ['HOST'], context.parameters['/prod/camelot/db-password']) as session:
        body = [as_dict(role) for role in session.query(Role).all()]
    return body

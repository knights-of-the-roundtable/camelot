import json

from models import Role
from db_util import db_session

def lambda_handler(event, context):
    body = None
    with db_session() as session:
        body = [role.name for role in session.query(Role).all()]
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

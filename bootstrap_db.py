import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Role, Outcome, Base

def bootstrap():
    engine = create_engine(
        'postgresql+auroradataapi://:@/tintagel',
        connect_args={
            'aurora_cluster_arn': 'arn:aws:rds:us-west-2:472965085233:cluster:albion-serverless',
            'secret_arn': 'arn:aws:secretsmanager:us-west-2:472965085233:secret:prod/camelot/albion-serverless-iINkbR'
        }
    )
    
    # Drops all tables comment in if you want to start clean
    Base.metadata.drop_all(engine)

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

    # Bootstrap data
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.add(Role(name='Mordred')) # 1
    session.add(Role(name='Morgana')) # 2
    session.add(Role(name='Oberon')) # 3 
    session.add(Role(name='Assassin')) # 4
    session.add(Role(name='Minion')) # 5
    session.add(Role(name='Merlin')) # 6
    session.add(Role(name='Percival')) # 7
    session.add(Role(name='Servant')) # 8

    session.add(Outcome(name='Blue Wins'))
    session.add(Outcome(name='Red Wins by Missions'))
    session.add(Outcome(name='Red Wins by Assassination'))
    session.add(Outcome(name='Red Wins by Rejected Votes'))

    session.commit()
    session.close()

if __name__ == "__main__":
    bootstrap()

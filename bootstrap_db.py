import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Role, Outcome, Base

engine = create_engine('postgresql://postgres:docker@localhost:5432')
 
# Drops all tables comment in if you want to start clean
# Base.metadata.drop_all(engine)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

# Bootstrap data
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
session.add(Role(name='Mordred'))
session.add(Role(name='Morgana'))
session.add(Role(name='Oberon'))
session.add(Role(name='Assassin'))
session.add(Role(name='Minion'))
session.add(Role(name='Merlin'))
session.add(Role(name='Percival'))

session.add(Outcome(name='Blue Wins'))
session.add(Outcome(name='Red Wins by Missions'))
session.add(Outcome(name='Red Wins by Assassination'))
session.add(Outcome(name='Red Wins by Rejected Votes'))

session.commit()
session.close()

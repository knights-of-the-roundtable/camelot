from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import func

Base = declarative_base()
 
class Player(Base):
    __tablename__ = 'players'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    __table_args__ = (UniqueConstraint(first_name, last_name, name="_first_last_uc"),)

    def __repr__(self):
        return "<Player(first_name='%s', last_name='%s')>" % (self.first_name, self.last_name)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)

    def is_good(self):
        return self.id > 5

    def __repr__(self):
        return self.name

class Outcome(Base):
    __tablename__ = 'outcomes'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    def is_good(self):
        return self.id == 1

    def __repr__(self):
        return self.name
 
class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    outcome_id = Column(Integer, ForeignKey(Outcome.id), nullable=False)
    outcome = relationship(Outcome)
    mvp_id = Column(Integer, ForeignKey(Player.id), nullable=False)
    mvp = relationship(Player, foreign_keys=mvp_id)
    lvp_id = Column(Integer, ForeignKey(Player.id), nullable=False)
    lvp = relationship(Player, foreign_keys=lvp_id)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    game_players = relationship("GamePlayer")

    def __repr__(self):
        return "<Game(outcome='%s', mvp='%s', lvp='%s', date='%s')>" % (self.outcome, self.mvp, self.lvp, self.date)

class GamePlayer(Base):
    __tablename__ = "gameplayers"
    game_id = Column(Integer, ForeignKey(Game.id), primary_key=True)
    player_id = Column(Integer, ForeignKey(Player.id), primary_key=True)
    player = relationship(Player)
    role_id = Column(Integer, ForeignKey(Role.id))
    role = relationship(Role)

    def __repr__(self):
        return "<GamePlayer(game_id='%s', player='%s', role='%s')>" % (self.game_id, self.player, self.role)

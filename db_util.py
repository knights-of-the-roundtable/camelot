from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

class db_session:
    def __init__(self, host, password):
        self.host = host
        self.password = password

    def __enter__(self):
        engine = create_engine('postgresql://postgres:%s@%s:5432' % (self.password, self.host))
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        return self.session

    def __exit__(self, type, value, traceback):
        if type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

def as_dict(model):
       return {c.name: str(getattr(model, c.name)) for c in model.__table__.columns}

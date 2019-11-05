from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

class db_session:
    def __enter__(self):
        engine = create_engine('postgresql://postgres:docker@localhost:5432')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        return self.session

    def __exit__(self, type, value, traceback):
        self.session.close()

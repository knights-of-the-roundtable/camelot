from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

class db_session:
    def __init__(self, aurora_cluster_arn, secret_arn):
        self.aurora_cluster_arn = aurora_cluster_arn
        self.secret_arn = secret_arn

    def __enter__(self):
        engine = create_engine(
            'postgresql+auroradataapi://:@/tintagel',
            connect_args={
                'aurora_cluster_arn': self.aurora_cluster_arn,
                'secret_arn': self.secret_arn
            }
        )
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

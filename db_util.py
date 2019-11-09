from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

class db_session:
    def __enter__(self):
        engine = create_engine(
            'postgresql+auroradataapi://:@/tintagel',
            connect_args={
                'aurora_cluster_arn': 'arn:aws:rds:us-west-2:472965085233:cluster:albion-serverless',
                'secret_arn': 'arn:aws:secretsmanager:us-west-2:472965085233:secret:prod/camelot/albion-serverless-iINkbR'
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

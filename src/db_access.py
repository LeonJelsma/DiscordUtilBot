from sqlalchemy import *

engine = create_engine('sqlite:///db.db')
metadata = MetaData()
Base = declarative_base()


def create_db_if_not_exist():
    RandomResponses = Table('RandomResponses', metadata,
                            Column('response_id', Integer, primary_key=True),
                            Column('message', String(60), nullable=False))
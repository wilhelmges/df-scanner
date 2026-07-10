from db import engine
from sqlalchemy import Index
from models.sqlmodels import Df1

def create_indexes(engine):
    indexes = [
        Index(
            "idx_df1_numident",
            Df1.__table__.c.NUMIDENT
        ),
        Index(
            "idx_df1_numident",
            Df1.__table__.c.NUMIDENT
        ),
    ]

    for idx in indexes:
        idx.create(bind=engine, checkfirst=True)

if __name__ == "__main__":
    print(engine.url)
    create_indexes(engine)

    #to check indexes after PRAGMA index_list('df1');

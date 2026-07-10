from db import engine
from sqlalchemy import Index, text
from models.sqlmodels import Df1, Df4, Df5

def delete_all_indexes(engine):
    with engine.begin() as conn:
        indexes = conn.execute(
            text("""
                SELECT name
                FROM sqlite_master
                WHERE type='index'
                  AND sql IS NOT NULL
            """)
        ).fetchall()

        for (index_name,) in indexes:
            conn.execute(text(f'DROP INDEX "{index_name}"'))
            print(f"Dropped: {index_name}")

def create_indexes(engine):
    indexes = [
        Index(
            "idx_df1_numident",
            Df1.__table__.c.NUMIDENT
        ),
        Index(
            "idx_df1_LN",
            Df1.__table__.c.LN
        ),
        Index(
            "idx_df1_NM",
            Df1.__table__.c.NM
        ),
        Index(
            "idx_df1_FTN",
            Df1.__table__.c.FTN
        ),
        Index(
            "idx_df1_SUM_TOTAL",
            Df1.__table__.c.SUM_TOTAL
        ),

        #Df4 indexes
        Index(
            "idx_df4_TIN",
            Df4.__table__.c.TIN
        ),
        Index(
            "idx_df4_S_NAR",
            Df4.__table__.c.S_NAR
        ),
        Index(
            "idx_df4_S_TAXN",
            Df4.__table__.c.S_TAXN
        ),

        #df5 indexes
        Index(
            "idx_df5_NUMIDENT",
            Df5.__table__.c.NUMIDENT
        ),
        Index(
            "idx_df5_LN",
            Df5.__table__.c.LN
        ),
        Index(
            "idx_df5_NM",
            Df5.__table__.c.NM
        ),
        Index(
            "idx_df5_FTN",
            Df5.__table__.c.FTN
        ),
        Index(
            "idx_df5_VZV",
            Df5.__table__.c.VZV
        ),
    ]

    for idx in indexes:
        idx.create(bind=engine, checkfirst=True)

if __name__ == "__main__":
    print(engine.url)
    #delete_all_indexes(engine)
    create_indexes(engine)

    #to check indexes after PRAGMA index_list('df1');

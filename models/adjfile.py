from sqlalchemy import Column, String

from db import Base

class Adjfile(Base):
    __tablename__ = "dfsource"
    __table_args__ = {
        "comment": ""
    }

    NUMIDENT = Column(String(10), comment="Шлях до уточнення", info={
       "length": 300, "label": "файл уточнення"
    })

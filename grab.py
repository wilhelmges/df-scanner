import dbf
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from models.dbf110 import Df1
from db import Base, engine, SessionLocal
from core import check_tax_code
from pathlib import Path

# C:\progs\df-scanner\samples\J0510409_4_2024.dbf  r"C:\progs\df-scanner\1 кв. 2023\Уточнення Гладишенко\J0510106_1_23_1.dbf"
def grab_df1(file: Path):
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()
    session = SessionLocal()

    for record in table:
        ipn=record.NUMIDENT
        # print(ipn)
        # if not ipn.isdigit():
        #     continue
        # if not check_tax_code(ipn):
        #     print(ipn, record.LN, record.NM)
        try:
            sumnarah=float(record.SUM_NARAH)
        except Exception as e:
            _error = str(e)
            sumnarah = float(record.SUM_NARAH.replace('\xa0', '').replace(' ', '').replace(',', '.'))


        session.add(Df1(
            NUMIDENT=record.NUMIDENT,
            PERIOD_M=record.PERIOD_M,
            PERIOD_Y=record.PERIOD_Y,
            PAY_TP=record.PAY_TP,
            PAY_MNTH=record.PAY_MNTH,
            PAY_YEAR=record.PAY_YEAR,
            LN=record.LN.capitalize(),
            NM=record.NM.capitalize(),
            SUM_NARAH=sumnarah,
            OZN=record.OZN,
        ))

    session.commit()

def check_df1(file: Path):
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()

    for num, record in enumerate(table, start=1):
        m = int(record.PERIOD_M)
        if m<1 or m>12:
            print(f"Помилка в рядку {num}: file = {str(file)}")




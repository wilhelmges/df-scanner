import dbf
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from models.dbf110 import Df1
from db import Base, engine, SessionLocal
from core import check_tax_code
from pathlib import Path
from collections import defaultdict


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

def load_dbf_rows(table):
    def normalize(value):
        if isinstance(value, str):
            value = value.strip()

        return value

    field_names = table.field_names

    rows = []

    for record in table:
        row = {
            field: normalize(record[field])
            for field in field_names
        }

        rows.append(row)

    used_fields = {
        field
        for row in rows
        for field, value in row.items()
        if value not in (None, '')
    }

    return [
        {
            field: value
            for field, value in row.items()
            if field in used_fields
        }
        for row in rows
    ]

def is_adjustment_for1person(rows):
    _={row['NUMIDENT'] for row in rows}
    if len(_)==1:
        return True

def apply_adjustment(file: Path):
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()

    for record in table:
        if record.OZN.isdigit() and (int(record.OZN)==1 or int(record.OZN)==0):
            continue
        #print(f"notfull 0,1 in {str(file)}")
        return
    print(f" letstry {str(file)}")
    session = SessionLocal()
    adj = load_dbf_rows(table)
    if is_adjustment_for1person(adj):
        print(adj); exit()





import dbf
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from models.dbf110 import Df1
from db import Base, engine, SessionLocal
from core import check_tax_code
from core import dbf_report_params
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
            NUMIDENT=str(record.NUMIDENT).strip(),
            PERIOD_M=record.PERIOD_M,
            PERIOD_Y=record.PERIOD_Y,
            PAY_TP=record.PAY_TP,
            PAY_MNTH=record.PAY_MNTH,
            PAY_YEAR=record.PAY_YEAR,
            LN=record.LN.capitalize().strip(),
            NM=record.NM.capitalize().strip(),
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

def get_different_fields(rows: list[dict]) -> dict:
    """
    Повертає словник:
    {
        "FIELD": [значення_по_рядках]
    }

    лише для тих полів, де є різні значення.
    """

    values_by_field = defaultdict(list)

    # збираємо значення полів
    for row in rows:
        for key, value in row.items():
            values_by_field[key].append(value)

    # залишаємо тільки поля з різними значеннями
    result = {
        key: values
        for key, values in values_by_field.items()
        if len(set(values)) > 1
    }

    return result

def is_adjustment_for1person(rows):
    _={row['NUMIDENT'] for row in rows}
    if len(_)==1:
        return True

def to_int(value, default=-1):
    if value is None:
        return default

    s = str(value).strip()

    if not s:
        return default

    return int(float(s))

def lookfor23(file: Path):
    table = dbf.Table(str(file), codepage='cp1251')
    print(str(file), dbf_report_params(str(file.stem)))
    table.open()
    dfnum = dbf_report_params(str(file.stem))
    for record in table:
        s = None
        num = -1
        sp = None
        pay_tp = -1

        if dfnum == 1 or dfnum == 5:
            s = record.OZN
            num = to_int(s)

        if dfnum == 4:
            s = record.OZNAKA
            num = to_int(s)

        if dfnum==1:
            sp = record.PAY_TP
            pay_tp = to_int(sp)
            print(s, num, sp, pay_tp)
        else:
            print(s, num)
        if num==2 or num==3:
            print(str(file))


def apply_adjustment(file: Path):
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()

    for record in table:
        #print('ozn '+record.OZN)
        if dbf_report_params(str(file))==1 or dbf_report_params(str(file))==5 and( (int(record.OZN)==2 or int(record.OZN)==3)):
            print(str(file))
        if dbf_report_params(str(file))==4 and ((int(record.OZNAKA)==2 or int(record.OZNAKA)==3)):
            print(str(file))
        #print(f"notfull 0,1 in {str(file)}")
    return
    # print(f" letstry {str(file)}")
    # session = SessionLocal()
    # adj = load_dbf_rows(table)
    # print(get_different_fields(adj))

    #
    # if is_adjustment_for1person(adj):
    #     print(adj); exit()





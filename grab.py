from decimal import Decimal

import dbf
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.orm import sessionmaker
from models.dbf110 import Df1
from models.dbf410 import Df4
from models.dbf510 import Df5
from db import Base, engine, SessionLocal
from core import check_tax_code, to_int, short_dbf_path
from core import dbf_report_params
from pathlib import Path
from collections import defaultdict
from repository import finddf1, find_df1_anddeleteifonlyone, add_df1
from repository import inc_or_create, dec_or_delete
from types import SimpleNamespace

from sanitizer import normalize_dbf_record
from df4_sanitizer import parse_dbf4_row
from df5_sanitizer import parse_dbf_record

# C:\progs\df-scanner\samples\J0510409_4_2024.dbf  r"C:\progs\df-scanner\1 кв. 2023\Уточнення Гладишенко\J0510106_1_23_1.dbf"
def grab_df1(file: Path):
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()
    session = SessionLocal()
    try:
        for record in table:
            rerec = normalize_dbf_record(record, as_object=True)
            #print(rerec.LN, rerec.PAY_TP, rerec.OZN, rerec.SUM_NARAH)
            add_df1(rerec, session)
        session.commit()

    except Exception as e:
        print(str(e), e)
        exit()

def grab_df4(file: Path):
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()
    session = SessionLocal()
    rerec = None
    try:
        for record in table:
            rerec = parse_dbf4_row(record)
            print(rerec.TIN, rerec.S_DOX)
            session.add(Df4(
                PERIOD=rerec.PERIOD,
                TIN=rerec.TIN,
                S_NAR=rerec.S_NAR,
                S_DOX=rerec.S_DOX,
                OZN_DOX=rerec.OZN_DOX,
            ))

    except Exception as e:
        if rerec is not None:
            print(rerec.TIN, str(file), str(e))
        else:
            print(str(file), str(e))

    finally:
        session.commit()
        session.close()

def grab_df5(file: Path):
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()
    session = SessionLocal()
    try:
        for record in table:
            rerec = parse_dbf_record(record)
            print(rerec.NUMIDENT, rerec.LN)
            session.add(Df5(
                PERIOD_M=rerec.PERIOD_M,
                PERIOD_Y=rerec.PERIOD_Y,
                NUMIDENT=rerec.NUMIDENT,
                LN=rerec.LN,
                NM=rerec.NM,
                FTN=rerec.FTN,
                START_DT=rerec.START_DT,
                END_DT=rerec.END_DT,
                PID=rerec.PID,
                VZV=rerec.VZV,
            ))
    except Exception as e:
        print(rerec.NUMIDENT, rerec.LN, str(file), str(e))
    finally:
        session.commit()
        session.close()


def lookfor23(file: Path):
    dfnum = dbf_report_params(str(file.stem))
    if dfnum != 1:
        return
    table = dbf.Table(str(file), codepage='cp1251')
    # print(str(file), dbf_report_params(str(file.stem)))
    table.open()
    sum01 = Decimal("0")
    for record in table:
        rerec = normalize_dbf_record(record, as_object=True)
        pay_tp = to_int(rerec.PAY_TP)
        ozn = to_int(rerec.OZN)
        if (pay_tp == 2 or pay_tp == 3) and (ozn==0 or ozn == 1):
            print('two operations ',rerec.NUMIDENT,rerec.LN, pay_tp, ozn, short_dbf_path(str(file)))
        elif not(pay_tp == 2 or pay_tp == 3) and (not(ozn == 0 or ozn == 1)):
            print('none operation ', rerec.NUMIDENT, rerec.LN, pay_tp, ozn, short_dbf_path(str(file)))
        elif rerec.SUM_NARAH is None:
            print('None sum_narah ',repr(rerec.SUM_NARAH), rerec.NUMIDENT, rerec.LN, short_dbf_path(str(file)))
        elif ozn==0 or ozn == 1:
            sign = -1 if ozn == 1 else 1 if ozn == 0 else None
            sum01+=Decimal(str(sign)) * Decimal(str(rerec.SUM_NARAH))
    if sum01 != 0:
        print('not zero sum ',sum01, short_dbf_path(str(file)))

def apply_df1_adjustment(file: Path):
    # if dbf_report_params(str(file.stem))!=1:
    #     return
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()

    try:
        with SessionLocal() as session:
            for record in table:
                rerec = normalize_dbf_record(record, as_object=True)
                ozn = to_int(rerec.OZN)
                pay_tp = to_int(rerec.PAY_TP)
                if pay_tp == 2:
                    inc_or_create(rerec, session)
                elif pay_tp == 3:
                    dec_or_delete(rerec, session)
                elif ozn == 1:
                    find_df1_anddeleteifonlyone(rerec, session)
                elif ozn == 0:
                    add_df1(rerec, session)
                else:
                    raise Exception('indefinite operation')
        session.commit()
    except MultipleResultsFound as e:
        print(rerec.NUMIDENT, rerec.LN, str(file), str(e))
        session.rollback()
        return None
    except Exception as e:
        print(rerec.NUMIDENT, rerec.LN, str(file), str(e))
        # session.rollback()
        # return None

    return 42

    # print(f" letstry {str(file)}")
    # session = SessionLocal()
    # adj = load_dbf_rows(table)
    # print(get_different_fields(adj))

    #
    # if is_adjustment_for1person(adj):
    #     print(adj); exit()

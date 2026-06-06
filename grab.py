from decimal import Decimal
import traceback
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
from repository import finddf1, find_df1_anddeleteifonlyone, add_df1, find_df5_anddeleteifonlyone, add_df5, \
    find_df4_anddeleteifonlyone, add_df4
from repository import inc_or_create, dec_or_delete
from types import SimpleNamespace

from df1_sanitizer import parse_dbf1_record
from df4_sanitizer import parse_dbf4_record
from df5_sanitizer import parse_dbf5_record

# C:\progs\df-scanner\samples\J0510409_4_2024.dbf  r"C:\progs\df-scanner\1 кв. 2023\Уточнення Гладишенко\J0510106_1_23_1.dbf"
def grab_df1(file: Path):
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()
    session = SessionLocal()
    try:
        for record in table:
            rerec = parse_dbf1_record(record, as_object=True)
            #print(rerec.LN, rerec.PAY_TP, rerec.OZN, rerec.SUM_NARAH)
            add_df1(rerec, session)
        session.commit()

    except Exception as e:
        print(str(e), e)
        print(traceback.format_exc())
        exit()

def grab_df4(file: Path):
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()
    session = SessionLocal()
    rerec = None
    try:
        for record in table:
            rerec = parse_dbf4_record(record)
            add_df4(rerec, session)

    except Exception as e:
        traceback.print_exc()
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
            rerec = parse_dbf5_record(record)
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
                rerec = parse_dbf1_record(record, as_object=True)
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

def apply_df4_adjustment(file: Path):
    if dbf_report_params(str(file.stem))!=4:
        return
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()

    rerec =None
    try:
        with SessionLocal() as session:
            for record in table:
                rerec = parse_dbf4_record(record)
                ozn = to_int(rerec.OZNAKA)
                ozn2 = to_int(rerec.OZNAKA2)
                ozn = max(ozn, ozn2)
                pay_tp = to_int(rerec.TYP)
                print('ozn', ozn,'typ ', pay_tp, short_dbf_path(str(file)))

                if ozn == 1:
                    find_df4_anddeleteifonlyone(rerec, session)
                elif ozn == 0:
                    add_df4(rerec, session)
                # if pay_tp == 2:
                #     inc_or_create(rerec, session)
                # elif pay_tp == 3:
                #     dec_or_delete(rerec, session)
                else:
                    raise Exception('indefinite operation')
        session.commit()
    except MultipleResultsFound as e:
        print(rerec.TIN, str(file), str(e))
        session.rollback()
        return None
    except Exception as e:
        print(str(file), str(e))
        # session.rollback()
        # return None

    return 42

def apply_df5_adjustment(file: Path):
    if dbf_report_params(str(file.stem))!=5:
        return
    table = dbf.Table(str(file), codepage='cp1251')
    table.open()

    try:
        with SessionLocal() as session:
            for record in table:
                rerec = parse_dbf5_record(record)
                ozn = to_int(rerec.OZN)
                if ozn == 1:
                    find_df5_anddeleteifonlyone(rerec, session)
                elif ozn == 0 or ozn==-1:
                    add_df5(rerec, session)
                else:
                    raise Exception('indefinite operation, ozn ', ozn)
        session.commit()
    except MultipleResultsFound as e:
        traceback.print_exc()
        print(rerec.NUMIDENT, rerec.LN, str(file), str(e))
        session.rollback()
        return None
    except Exception as e:
        traceback.print_exc()
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

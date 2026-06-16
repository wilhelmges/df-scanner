import pathlib
from pathlib import Path

from core import dbf_report_params
from db import SessionLocal

def process_file(str_file_path, main=False):
    file = Path(str_file_path)
    dbftype = dbf_report_params(file.stem)
    print(dbftype)

def canbe_imported(file: pathlib.Path) -> bool:
    rez = None
    if file.suffix != ".dbf":
        return False
    file_content = file.rea
    session = SessionLocal()




if __name__ == "__main__":
    filename = r'C:\progs\df-scanner\samples\updates\J0510110_26_01.dbf'
    process_file(filename)

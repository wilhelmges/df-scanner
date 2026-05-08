from sqlalchemy import Column, Integer, String, Numeric
from db import Base

class EmployeeRecord(Base):
    __tablename__ = "employee_records"

    id = Column(Integer, primary_key=True, autoincrement=True)

    PERIOD_M = Column(
        Numeric(4, 2),
        comment="Місяць періоду"
    )

    PERIOD_Y = Column(
        Numeric(7, 2),
        comment="Рік періоду"
    )

    UKR_GROMAD = Column(
        Numeric(4, 2),
        comment="Ознака громадянства України"
    )

    ZO = Column(
        Numeric(4, 2),
        comment="Код категорії"
    )

    DOG_CPH = Column(
        String(1),
        comment="Ознака договору ЦПХ"
    )

    NUMIDENT = Column(
        String(14),
        index=True,
        comment="Ідентифікаційний номер"
    )

    LN = Column(
        String(30),
        comment="Прізвище"
    )

    NM = Column(
        String(10),
        comment="Ім'я"
    )

    FTN = Column(
        String(15),
        comment="По батькові"
    )

    START_DT = Column(
        String(10),
        comment="Дата початку"
    )

    END_DT = Column(
        Date,
        comment="Дата завершення"
    )

    NRM_DT = Column(
        String(1),
        comment="Ознака нормованого часу"
    )

    PID_ZV = Column(
        String(1),
        comment="Підстава звільнення"
    )

    PNR = Column(
        String(1),
        comment="Ознака ПНР"
    )

    PROF = Column(
        String(1),
        comment="Професія"
    )

    POS = Column(
        String(1),
        comment="Посада"
    )

    PID = Column(
        String(48),
        comment="Ідентифікатор запису"
    )

    VZV = Column(
        String(30),
        comment="Назва виду зайнятості"
    )

    VS = Column(
        String(1),
        comment="Ознака VS"
    )

    PIR = Column(
        String(1),
        comment="Ознака PIR"
    )

    OZN = Column(
        String(1),
        comment="Ознака"
    )
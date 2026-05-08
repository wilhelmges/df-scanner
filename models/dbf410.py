from sqlalchemy import Column, String, Numeric, Integer
from db import Base

class PaymentRecord(Base):
    __tablename__ = "payment_records"

    id = Column(Integer, primary_key=True, autoincrement=True)

    PERIOD = Column(
        String(1),
        comment="Період"
    )

    RIK = Column(
        Numeric(7, 2),
        comment="Рік"
    )

    KOD = Column(
        String(1),
        comment="Код"
    )

    TYP = Column(
        Numeric(4, 2),
        comment="Тип"
    )

    TIN = Column(
        String(14),
        index=True,
        comment="Податковий номер / ІПН"
    )

    S_NAR = Column(
        Numeric(10, 2),
        comment="Сума нарахованого доходу"
    )

    S_DOX = Column(
        Numeric(10, 2),
        comment="Сума виплаченого доходу"
    )

    S_TAXN = Column(
        Numeric(9, 2),
        comment="Сума нарахованого податку"
    )

    S_TAXP = Column(
        Numeric(9, 2),
        comment="Сума перерахованого податку"
    )

    OZN_DOX = Column(
        Numeric(6, 2),
        comment="Ознака доходу"
    )

    D_PRIYN = Column(
        String(1),
        comment="Дата прийняття"
    )

    D_ZVILN = Column(
        String(1),
        comment="Дата звільнення"
    )

    OZN_PILG = Column(
        String(1),
        comment="Ознака пільги"
    )

    OZNAKA = Column(
        String(1),
        comment="Ознака"
    )

    A051 = Column(
        String(9),
        comment="Додаткове поле A051"
    )

    A05 = Column(
        String(9),
        comment="Додаткове поле A05"
    )

    D_ZVILN2 = Column(
        String(1),
        comment="Дата звільнення 2"
    )

    OZN_PILG2 = Column(
        String(1),
        comment="Ознака пільги 2"
    )

    OZNAKA2 = Column(
        String(1),
        comment="Ознака 2"
    )
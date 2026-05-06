from sqlalchemy import Column, Integer, String, Numeric
from db import Base

class PaymentRecord(Base):
    __tablename__ = "payment_records"
    __table_args__ = {
        "comment": "Імпорт з dBase III Plus: реєстр нарахувань/виплат"
    }

    id = Column(Integer, primary_key=True, autoincrement=True)

    PERIOD_M = Column(Integer, comment="Місяць звітного періоду", info={
        "dbf_type": "N", "length": 2, "scale": 0, "label": "Місяць періоду"
    })

    PERIOD_Y = Column(Integer, comment="Рік звітного періоду", info={
        "dbf_type": "N", "length": 4, "scale": 0, "label": "Рік періоду"
    })

    UKR_GROMAD = Column(Integer, comment="Ознака громадянства України", info={
        "dbf_type": "N", "length": 1, "scale": 0, "label": "Громадянин України",
        "hint": "0/1"
    })

    ST = Column(Integer, comment="Статус (не уточнено)", info={
        "dbf_type": "N", "length": 1, "scale": 0, "label": "Статус"
    })

    NUMIDENT = Column(String(10), comment="Ідентифікаційний номер", info={
        "dbf_type": "C", "length": 10, "label": "ІПН / ID"
    })

    LN = Column(String(100), comment="Прізвище", info={
        "dbf_type": "C", "length": 100, "label": "Прізвище"
    })

    NM = Column(String(100), comment="Ім’я", info={
        "dbf_type": "C", "length": 100, "label": "Ім’я"
    })

    FTN = Column(String(100), comment="По батькові", info={
        "dbf_type": "C", "length": 100, "label": "По батькові"
    })

    ZO = Column(Integer, comment="Ознака/зона (не уточнено)", info={
        "dbf_type": "N", "length": 2, "scale": 0, "label": "ZO"
    })

    PAY_TP = Column(Integer, comment="Тип виплати", info={
        "dbf_type": "N", "length": 3, "scale": 0, "label": "Тип виплати"
    })

    PAY_MNTH = Column(Integer, comment="Місяць виплати", info={
        "dbf_type": "N", "length": 2, "scale": 0, "label": "Місяць виплати"
    })

    PAY_YEAR = Column(Integer, comment="Рік виплати", info={
        "dbf_type": "N", "length": 4, "scale": 0, "label": "Рік виплати"
    })

    SUM_TOTAL = Column(Numeric(16, 2), comment="Загальна сума", info={
        "dbf_type": "N", "length": 16, "scale": 2, "label": "Загальна сума",
        "unit": "UAH"
    })

    SUM_MAX = Column(Numeric(16, 2), comment="Максимальна база/сума", info={
        "dbf_type": "N", "length": 16, "scale": 2, "label": "Макс. сума",
        "unit": "UAH"
    })

    SUM_INS = Column(Numeric(16, 2), comment="Сума страхових внесків", info={
        "dbf_type": "N", "length": 16, "scale": 2, "label": "Страхові внески",
        "unit": "UAH"
    })

    OTK = Column(Integer, comment="Ознака ОТК (не уточнено)", info={
        "dbf_type": "N", "length": 1, "scale": 0, "label": "OTK"
    })

    EXP = Column(Integer, comment="Ознака виключення/експорту", info={
        "dbf_type": "N", "length": 1, "scale": 0, "label": "EXP"
    })

    KD_NP = Column(Integer, comment="Кількість днів (NP)", info={
        "dbf_type": "N", "length": 2, "scale": 0, "label": "Дні NP"
    })

    KD_NZP = Column(Integer, comment="Кількість днів (NZP)", info={
        "dbf_type": "N", "length": 2, "scale": 0, "label": "Дні NZP"
    })

    KD_PTV = Column(Integer, comment="Кількість днів (PTV)", info={
        "dbf_type": "N", "length": 3, "scale": 0, "label": "Дні PTV"
    })

    NRM = Column(Integer, comment="Норматив (не уточнено)", info={
        "dbf_type": "N", "length": 1, "scale": 0, "label": "NRM"
    })

    KD_VP = Column(Integer, comment="Кількість днів (VP)", info={
        "dbf_type": "N", "length": 3, "scale": 0, "label": "Дні VP"
    })

    SUM_DIFF = Column(Numeric(16, 2), comment="Різниця сум", info={
        "dbf_type": "N", "length": 16, "scale": 2, "label": "Різниця",
        "unit": "UAH"
    })

    SUM_NARAH = Column(Numeric(16, 2), comment="Сума нарахувань", info={
        "dbf_type": "N", "length": 16, "scale": 2, "label": "Нараховано",
        "unit": "UAH"
    })

    NRC = Column(Integer, comment="Ознака NRC (не уточнено)", info={
        "dbf_type": "N", "length": 1, "scale": 0, "label": "NRC"
    })

    OZN = Column(String(1), comment="Ознака", info={
        "dbf_type": "C", "length": 1, "label": "Ознака"
    })

    OTD = Column(String(1), comment="Відділ/код", info={
        "dbf_type": "C", "length": 1, "label": "Відділ"
    })
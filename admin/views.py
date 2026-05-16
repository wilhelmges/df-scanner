from sqladmin import ModelView, BaseView, expose

from models.dbf110 import Df1
from models.dbf410 import Df4
from models.dbf510 import Df5

class Df1Admin(ModelView, model=Df1):
    name = "Df1"
    name_plural = "Df1"
    category = "Основні таблиці"

    column_list = [Df1.PAY_YEAR, Df1.PAY_MNTH, Df1.NUMIDENT, Df1.LN, Df1.NM, Df1.FTN,
                   Df1.SUM_TOTAL, Df1.SUM_MAX, Df1.SUM_NARAH
        , Df1.id]

    column_labels = {
        Df1.NUMIDENT: Df1.NUMIDENT.comment,
        Df1.LN: Df1.LN.comment,
        Df1.NM: Df1.NM.comment,
        Df1.FTN: Df1.FTN.comment,
        Df1.SUM_TOTAL: Df1.SUM_TOTAL.comment,
        Df1.SUM_MAX: Df1.SUM_MAX.comment,
        Df1.SUM_NARAH: Df1.SUM_NARAH.comment,
        Df1.PAY_YEAR: Df1.PAY_YEAR.comment,
        Df1.PAY_MNTH: Df1.PAY_MNTH.comment,
    }

    # Пошук
    column_searchable_list = [
        Df1.NUMIDENT,
        Df1.LN,
    ]

class Df4Admin(ModelView, model=Df4):
    name = "Df4"
    name_plural = "Df4"
    category = "Основні таблиці"

    column_list = [
        Df4.id,
        Df4.PERIOD,
        Df4.S_NAR,
        Df4.S_DOX,
        Df4.OZN_DOX,
    ]

    column_labels = {
        Df4.id: "ID",
        Df4.NP: "№",
        Df4.RIK: "Рік",
        Df4.PERIOD: "Місяць",
        Df4.KOD: "Код",
        Df4.TYP: "Тип",
        Df4.TIN: "ІПН",
        Df4.S_NAR: "Нараховано",
        Df4.S_DOX: "Виплачено",
        Df4.S_TAXN: "Податок нарах.",
        Df4.S_TAXP: "Податок перерах.",
        Df4.OZN_DOX: "Ознака доходу",
        Df4.D_PRIYN: "Дата прийняття",
        Df4.D_ZVILN: "Дата звільнення",
        Df4.OZN_PILG: "Пільга",
        Df4.OZNAKA: "Ознака",
        Df4.A051: "A051",
        Df4.A05: "A05",
    }

class Df5Admin(ModelView, model=Df5):
    name = "Df5"
    name_plural = "Df5"
    category = "Основні таблиці"

    # Відображення колонок у списку
    column_list = [
        Df5.id,
        Df5.PERIOD_Y,
        Df5.PERIOD_M,
        Df5.NUMIDENT,
        Df5.LN,
        Df5.NM,
        Df5.FTN,
        Df5.START_DT,
        Df5.END_DT,
    ]

    # Пошук
    column_searchable_list = [
        Df5.NUMIDENT,
        Df5.LN,
    ]


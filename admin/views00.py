from sqladmin import ModelView

from models.dbf110 import Df1
from models.dbf410 import Df4
from models.dbf510 import Df5

class Df1Admin(ModelView, model=Df1):
    column_list = [Df1.PAY_YEAR, Df1.PAY_MNTH, Df1.NUMIDENT, Df1.LN, Df1.NM,
                   Df1.SUM_TOTAL, Df1.SUM_MAX, Df1.SUM_NARAH
                   ,Df1.id]

    column_labels = {
        Df1.NUMIDENT: Df1.NUMIDENT.comment,
        Df1.LN: Df1.LN.comment,
        Df1.NM: Df1.NM.comment,
        Df1.SUM_TOTAL: Df1.SUM_TOTAL.comment,
        Df1.SUM_MAX: Df1.SUM_MAX.comment,
        Df1.SUM_NARAH: Df1.SUM_NARAH.comment,
        Df1.PAY_YEAR: Df1.PAY_YEAR.comment,
        Df1.PAY_MNTH: Df1.PAY_MNTH.comment,
    }

    # пошук
    column_searchable_list = [
        Df1.NUMIDENT,
    ]

    name = "Запис"
    name_plural = "Df1s"

    icon = "fa-solid fa-money-bill"

class Df4Admin(ModelView, model=Df4):
    """
    Admin view для таблиці Df4.
    """

    name = "Запис"
    name_plural = "Df4s"

    icon = "fa-solid fa-database"

    # -------------------------
    # Відображення колонок
    # -------------------------

    column_list = [
        Df4.id,
        Df4.RIK,
        Df4.PERIOD,
        Df4.TIN,
        Df4.KOD,
        Df4.TYP,
        Df4.S_NAR,
        Df4.S_DOX,
        Df4.S_TAXN,
        Df4.S_TAXP,
        Df4.OZN_DOX,
        Df4.OZN_PILG,
        Df4.D_PRIYN,
        Df4.D_ZVILN,
        Df4.OZNAKA,
    ]

    # -------------------------
    # Назви колонок
    # -------------------------

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

    # -------------------------
    # Пошук
    # -------------------------

    column_searchable_list = [
        Df4.TIN,
        Df4.KOD,
    ]

    # -------------------------
    # Сортування
    # -------------------------

    column_sortable_list = [
        Df4.id,
        Df4.RIK,
        Df4.PERIOD,
        Df4.TIN,
        Df4.S_NAR,
        Df4.S_DOX,
    ]

    # -------------------------
    # Детальний перегляд
    # -------------------------

    can_view_details = True

    details_columns = [
        Df4.id,
        Df4.NP,
        Df4.RIK,
        Df4.PERIOD,
        Df4.KOD,
        Df4.TYP,
        Df4.TIN,
        Df4.S_NAR,
        Df4.S_DOX,
        Df4.S_TAXN,
        Df4.S_TAXP,
        Df4.OZN_DOX,
        Df4.D_PRIYN,
        Df4.D_ZVILN,
        Df4.OZN_PILG,
        Df4.OZNAKA,
        Df4.A051,
        Df4.A05,
    ]

    # -------------------------
    # Pagination
    # -------------------------

    page_size = 100
    page_size_options = [25, 50, 100, 250, 500]

    # -------------------------
    # Permissions
    # -------------------------

    can_create = False
    can_edit = False
    can_delete = False

class Df5Admin(ModelView, model=Df5):
    name = "Запис"
    name_plural = "Df5s"

    icon = "fa-solid fa-briefcase"

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

    # Колонки у формі редагування
    form_columns = [
        Df5.PERIOD_Y,
        Df5.PERIOD_M,
        Df5.UKR_GROMAD,
        Df5.NUMIDENT,
        Df5.LN,
        Df5.NM,
        Df5.FTN,
        Df5.START_DT,
        Df5.END_DT,
        Df5.ZO,
        Df5.PID_ZV,
        Df5.NRM_DT,
        Df5.DOG_CPH,
        Df5.PNR,
        Df5.PROF,
        Df5.POS,
        Df5.PID,
        Df5.VZV,
        Df5.VS,
        Df5.PIR,
        Df5.OZN,
    ]

    # Пошук
    column_searchable_list = [
        Df5.NUMIDENT,
        Df5.LN,
    ]


    # Назви колонок
    column_labels = {
        Df5.id: "ID",
        Df5.PERIOD_M: "Місяць",
        Df5.PERIOD_Y: "Рік",
        Df5.UKR_GROMAD: "Громадянство",
        Df5.NUMIDENT: "ІПН",
        Df5.LN: "Прізвище",
        Df5.NM: "Ім’я",
        Df5.FTN: "По батькові",
        Df5.START_DT: "Початок роботи",
        Df5.END_DT: "Завершення роботи",
        Df5.ZO: "Категорія ЗО",
        Df5.PID_ZV: "Підстава звільнення",
        Df5.NRM_DT: "Дата документа",
        Df5.DOG_CPH: "ЦПХ",
        Df5.PNR: "Професія",
        Df5.PROF: "Код професії",
        Df5.POS: "Посада",
        Df5.PID: "Підстава прийняття",
        Df5.VZV: "Вид зайнятості",
        Df5.VS: "Військова служба",
        Df5.PIR: "Пільга",
        Df5.OZN: "Ознака",
    }

    # Пагінація
    page_size = 50
    page_size_options = [25, 50, 100, 250]

    # Дозволи
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    # Детальний перегляд
    details_exclude_list = []

    # Експорт
    can_export = True
    export_max_rows = 100000

    # Назви в експорті
    export_types = ["csv", "json"]
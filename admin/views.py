from sqladmin import ModelView

from models.dbf110 import Df1

class Df1Admin(ModelView, model=Df1):
    column_list = [Df1.id, Df1.NUMIDENT, Df1.LN, Df1.NM, Df1.SUM_NARAH]

    column_labels = {
        Df1.NUMIDENT: Df1.NUMIDENT.comment,
        Df1.LN: Df1.LN.comment,
        Df1.NM: Df1.NM.comment,
        Df1.SUM_NARAH: Df1.SUM_NARAH.comment,
    }

    # пошук
    column_searchable_list = [
        Df1.NUMIDENT,
    ]

    name = "Df1"
    name_plural = "Df1s"

    icon = "fa-solid fa-money-bill"
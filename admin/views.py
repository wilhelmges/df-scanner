from sqladmin import ModelView

from models.dbf110 import PaymentRecord

class PaymentRecordAdmin(ModelView, model=PaymentRecord):
    column_list = [PaymentRecord.id, PaymentRecord.NUMIDENT, PaymentRecord.LN, PaymentRecord.NM, PaymentRecord.SUM_NARAH]

    column_labels = {
        PaymentRecord.NUMIDENT: PaymentRecord.NUMIDENT.comment,
        PaymentRecord.LN: PaymentRecord.LN.comment,
        PaymentRecord.NM: PaymentRecord.NM.comment,
        PaymentRecord.SUM_NARAH: PaymentRecord.SUM_NARAH.comment,
    }

    name = "PaymentRecord"
    name_plural = "PaymentRecords"

    icon = "fa-solid fa-money-bill"
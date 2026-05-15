from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any


@dataclass(slots=True)
class DfRow:
    """
    Один рядок таблиці dBase III Plus.
    """

    # Порядковий номер запису
    NP: int | None

    # Місяць звітного періоду
    PERIOD: int | None

    # Рік звітного періоду
    RIK: int | None

    # Код / ідентифікатор запису
    KOD: str

    # Тип запису
    TYP: int | None

    # ІПН / податковий номер
    TIN: str

    # Сума нарахованого доходу
    S_NAR: Decimal | None

    # Сума виплаченого доходу
    S_DOX: Decimal | None

    # Сума нарахованого податку
    S_TAXN: Decimal | None

    # Сума перерахованого податку
    S_TAXP: Decimal | None

    # Ознака доходу
    OZN_DOX: int | None

    # Дата прийняття
    D_PRIYN: date | None

    # Дата звільнення
    D_ZVILN: date | None

    # Ознака пільги
    OZN_PILG: int | None

    # Додаткова ознака
    OZNAKA: str

    # Поле A051
    A051: Decimal | None

    # Поле A05
    A05: Decimal | None


def safe_str(value: Any, lower: bool = True) -> str:
    """
    Безпечне перетворення в строку.
    - None -> ""
    - прибирає пробіли
    - optionally переводить у lower-case
    """

    if value is None:
        return ""

    result = str(value).strip()

    # прибираємо null-символи
    result = result.replace("\x00", "")

    if lower:
        result = result.lower()

    return result


def safe_int(value: Any) -> int | None:
    """
    Безпечне перетворення в int.

    Підтримує:
    - int
    - float
    - bytes
    - строки
    - биті DBF значення
    """

    if value is None:
        return None

    # already int
    if isinstance(value, int):
        return value

    # bytes from broken DBF fields
    if isinstance(value, (bytes, bytearray)):
        try:
            value = value.decode("cp1251", errors="ignore")
        except Exception:
            return None

    text = str(value).strip()

    # empty
    if not text:
        return None

    # DBF null garbage
    text = text.replace("\x00", "").strip()

    if not text:
        return None

    # normalize decimal separator
    text = text.replace(",", ".")

    try:
        return int(float(text))
    except (ValueError, TypeError):
        return None


def safe_decimal(value: Any) -> Decimal | None:
    """
    Безпечне перетворення в Decimal.

    Підтримує:
    - 12345.67
    - 12 345,67
    - 12\xa0345,67
    """

    if value is None:
        return None

    if isinstance(value, Decimal):
        return value

    text = str(value).strip()

    if not text:
        return None

    # прибираємо пробіли та non-breaking space
    text = text.replace(" ", "")
    text = text.replace("\xa0", "")

    # заміна коми на крапку
    text = text.replace(",", ".")

    try:
        return Decimal(text)
    except (InvalidOperation, ValueError):
        return None


def safe_date(value: Any) -> date | None:
    """
    Безпечне перетворення в date.
    """

    if value is None:
        return None

    if isinstance(value, date):
        return value

    text = str(value).strip()

    if not text:
        return None

    formats = [
        "%Y-%m-%d",
        "%d.%m.%Y",
        "%Y%m%d",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    return None


def parse_dbf4_row(record: Any) -> DfRow:
    """
    Безпечне зчитування одного рядка DBF в Python-об'єкт.

    record:
        Об'єкт рядка DBF.
        Наприклад запис з dbfread або dbf.
    """

    return DfRow(
        NP=safe_int(getattr(record, "NP", None)),
        PERIOD=safe_int(getattr(record, "PERIOD", None)),
        RIK=safe_int(getattr(record, "RIK", None)),
        KOD=safe_str(getattr(record, "KOD", None)),
        TYP=safe_int(getattr(record, "TYP", None)),
        TIN=safe_str(getattr(record, "TIN", None)),
        S_NAR=safe_decimal(getattr(record, "S_NAR", None)),
        S_DOX=safe_decimal(getattr(record, "S_DOX", None)),
        S_TAXN=safe_decimal(getattr(record, "S_TAXN", None)),
        S_TAXP=safe_decimal(getattr(record, "S_TAXP", None)),
        OZN_DOX=safe_int(getattr(record, "OZN_DOX", None)),
        D_PRIYN=safe_date(getattr(record, "D_PRIYN", None)),
        D_ZVILN=safe_date(getattr(record, "D_ZVILN", None)),
        OZN_PILG=safe_int(getattr(record, "OZN_PILG", None)),
        OZNAKA=safe_str(getattr(record, "OZNAKA", None)),
        A051=safe_decimal(getattr(record, "A051", None)),
        A05=safe_decimal(getattr(record, "A05", None)),
    )
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

    # Додаткова ознака
    OZNAKA2: str

    # Поле A051
    A051: Decimal | None

    # Поле A05
    A05: Decimal | None


def get_field(record: Any, name: str) -> Any:
    """
    Безпечне отримання поля з DBF-запису.
    """

    if record is None:
        return None

    # dict-like
    if isinstance(record, dict):
        return record.get(name)

    # object-like
    try:
        return getattr(record, name)
    except Exception:
        return None

def safe_str(value: Any, lower: bool = True) -> str:
    """
    Безпечне перетворення в строку.

    - None -> ""
    - bytes -> decode cp1251
    - trim
    - remove null-bytes
    - optionally lower-case
    """

    if value is None:
        return ""

    if isinstance(value, (bytes, bytearray)):
        try:
            value = value.decode("cp1251", errors="ignore")
        except Exception:
            return ""

    result = str(value)

    # remove null-bytes
    result = result.replace("\x00", "")

    # trim
    result = result.strip()

    if lower:
        result = result.lower()

    return result


def safe_int(value: Any) -> int | None:
    if value is None:
        return None

    if isinstance(value, int):
        return value

    if isinstance(value, (bytes, bytearray)):
        # якщо поле повністю забите null-byte
        if not value.replace(b"\x00", b""):
            return None

        try:
            value = value.decode("cp1251", errors="ignore")
        except Exception:
            return None

    text = str(value)

    text = text.replace("\x00", "")
    text = text.strip()

    if not text:
        return None

    text = text.replace(",", ".")

    try:
        return int(Decimal(text))
    except Exception:
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

    if isinstance(value, (bytes, bytearray)):
        try:
            value = value.decode("cp1251", errors="ignore")
        except Exception:
            return None

    text = str(value)

    text = text.replace("\x00", "")
    text = text.replace(" ", "")
    text = text.replace("\xa0", "")
    text = text.strip()

    if not text:
        return None

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

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if isinstance(value, (bytes, bytearray)):
        try:
            value = value.decode("cp1251", errors="ignore")
        except Exception:
            return None

    text = str(value)

    text = text.replace("\x00", "")
    text = text.strip()

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


def parse_dbf4_record(record: Any) -> DfRow:
    """
    Безпечне перетворення DBF-запису в DfRow.
    """

    return DfRow(
        NP=safe_int(get_field(record, "NP")),
        PERIOD=safe_int(get_field(record, "PERIOD")),
        RIK=safe_int(get_field(record, "RIK")),

        KOD=safe_str(get_field(record, "KOD"), lower=False),

        TYP=safe_int(get_field(record, "TYP")),

        TIN=safe_str(get_field(record, "TIN"), lower=False),

        S_NAR=safe_decimal(get_field(record, "S_NAR")),
        S_DOX=safe_decimal(get_field(record, "S_DOX")),
        S_TAXN=safe_decimal(get_field(record, "S_TAXN")),
        S_TAXP=safe_decimal(get_field(record, "S_TAXP")),

        OZN_DOX=safe_int(get_field(record, "OZN_DOX")),

        D_PRIYN=safe_date(get_field(record, "D_PRIYN")),
        D_ZVILN=safe_date(get_field(record, "D_ZVILN")),

        OZN_PILG=safe_int(get_field(record, "OZN_PILG")),

        OZNAKA=safe_str(get_field(record, "OZNAKA"), lower=False),
        OZNAKA2=safe_str(get_field(record, "OZNAKA2"), lower=False),

        A051=safe_decimal(get_field(record, "A051")),
        A05=safe_decimal(get_field(record, "A05")),
    )
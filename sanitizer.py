from __future__ import annotations

from decimal import Decimal, InvalidOperation
from types import SimpleNamespace
from typing import Any
import re


# --- конфігурація полів ------------------------------------------------------

INT_FIELDS = {
    "PERIOD_M",
    "PERIOD_Y",
    "UKR_GROMAD",
    "ST",
    "ZO",
    "PAY_MNTH",
    "PAY_YEAR",
    "KD_PTV",
}

FLOAT_FIELDS = {
    "SUM_TOTAL",
    "SUM_MAX",
    "SUM_NARAH",
}

STRING_FIELDS = {
    "NUMIDENT",
    "LN",
    "NM",
    "FTN",
    "PAY_TP",
    "KD_NP",
    "KD_NZP",
    "KD_VP",
    "SUM_DIFF",
    "SUM_INS",
    "OTK",
    "EXP",
    "NRC",
    "NRM",
    "OZN",
}


# --- допоміжні функції -------------------------------------------------------

def _clean_string(value: Any) -> str | None:
    """
    Безпечна очистка строк:
    - None -> None
    - trim
    - lower()
    - видалення control chars
    - кілька пробілів -> один
    - порожня строка -> None
    """

    if value is None:
        return None

    try:
        s = str(value)
    except Exception:
        return None

    # прибрати control chars
    s = re.sub(r"[\x00-\x1f\x7f]", "", s)

    # trim
    s = s.strip()

    # collapse spaces
    s = re.sub(r"\s+", " ", s)

    # lower
    s = s.lower()

    if s == "":
        return None

    return s


def _safe_decimal(value: Any) -> Decimal | None:
    """
    Максимально безпечне перетворення в Decimal.
    """

    if value is None:
        return None

    if isinstance(value, Decimal):
        return value

    try:
        s = str(value).strip()

        if s == "":
            return None

        # legacy артефакти
        s = s.replace(",", ".")

        return Decimal(s)

    except (InvalidOperation, ValueError, TypeError):
        return None


def _safe_int(value: Any) -> int | None:
    """
    Безпечне перетворення:
    2025.00 -> 2025
    '02' -> 2
    '' -> None
    """

    dec = _safe_decimal(value)

    if dec is None:
        return None

    try:
        return int(dec)
    except Exception:
        return None


def _safe_float(value: Any) -> float | None:
    dec = _safe_decimal(value)

    if dec is None:
        return None

    try:
        return float(dec)
    except Exception:
        return None


# --- головна функція ---------------------------------------------------------

def normalize_dbf_record(
    record,
    as_object: bool = False,
    keep_unknown_fields: bool = True,
):

    result = {}

    # правильне отримання назв полів dbf.Record
    try:
        field_names = list(record._meta.fields)
    except Exception:
        raise ValueError("Cannot extract DBF field names")

    for field in field_names:

        try:
            raw_value = record[field]
        except Exception:
            raw_value = None

        field_upper = field.upper()

        if field_upper in INT_FIELDS:
            value = _safe_int(raw_value)

        elif field_upper in FLOAT_FIELDS:
            value = _safe_float(raw_value)

        elif field_upper in STRING_FIELDS:
            value = _clean_string(raw_value)

        else:
            if keep_unknown_fields:
                value = _clean_string(raw_value)
            else:
                continue

        result[field] = value

    if as_object:
        return SimpleNamespace(**result)

    return result

if __name__ == "__main__":
    import dbf

    table = dbf.Table("test.dbf", codepage="cp1251")
    table.open()

    for record in table:
        # dict
        row = normalize_dbf_record(record)

        print(row["numident"])
        print(row["period_y"])

        # object
        obj = normalize_dbf_record(record, as_object=True)

        print(obj.numident)
        print(obj.period_y)
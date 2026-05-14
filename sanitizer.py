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
    "PAY_TP",
    "OZN",
}

FLOAT_FIELDS = {
    "SUM_TOTAL",
    "SUM_MAX",
    "SUM_NARAH",
    "SUM_DIFF",
    "SUM_INS",
}

STRING_FIELDS = {
    "NUMIDENT",
    "LN",
    "NM",
    "FTN",

    "KD_NP",
    "KD_NZP",
    "KD_VP",

    "OTK",
    "EXP",
    "NRC",
    "NRM",

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

    # кілька пробілів -> один
    s = re.sub(r"\s+", " ", s)

    # нижній регістр
    s = s.lower()

    if s == "":
        return None

    return s


def _safe_decimal(value: Any) -> Decimal | None:

    if value is None:
        return None

    try:

        if isinstance(value, Decimal):
            return value

        s = str(value).strip()

        if not s:
            return None

            # прибрати всі пробіли включно з NBSP
            s = s.replace("\xa0", "")
            s = s.replace(" ", "")

            # legacy формат
            s = s.replace(",", ".")

        return Decimal(s)

    except Exception:
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

    if value is None:
        return None

    try:

        # Decimal/int/float
        if isinstance(value, (Decimal, int, float)):
            return float(value)

        s = str(value).strip()

        if not s:
            return None

        # прибрати всі пробіли включно з NBSP
        s = s.replace("\xa0", "")
        s = s.replace(" ", "")

        # legacy формат
        s = s.replace(",", ".")

        return float(s)

    except Exception:
        return None


# --- головна функція ---------------------------------------------------------

def normalize_dbf_record(
    record,
    as_object: bool = False,
    keep_unknown_fields: bool = True,
):
    """
    Нормалізація DBF record.

    Parameters
    ----------
    record:
        рядок з dbf.Table

    as_object:
        False -> dict
        True  -> SimpleNamespace з доступом через крапку

    keep_unknown_fields:
        якщо True — невідомі поля також будуть включені

    Returns
    -------
    dict | SimpleNamespace
    """

    result = {}

    # правильне отримання назв полів для dbf.Record
    try:
        field_names = list(record._meta.fields)
    except Exception as e:
        raise ValueError(f"Cannot extract DBF field names: {e}")

    for field in field_names:

        try:
            raw_value = record[field]
        except Exception:
            raw_value = None

        field_upper = field.upper()

        # PAY_TP: пусте значення -> 0
        if field_upper == "PAY_TP":

            value = _safe_int(raw_value)

            if value is None:
                value = 0

        # OZN: пусте значення або пробіли -> -1
        elif field_upper == "OZN":
            value = _safe_int(raw_value)
            if value is None:
                value = -1

        # integer поля
        elif field_upper in INT_FIELDS:
            value = _safe_int(raw_value)

        # float поля
        elif field_upper in FLOAT_FIELDS:
            value = _safe_float(raw_value)

        # string поля
        elif field_upper in STRING_FIELDS:
            value = _clean_string(raw_value)

        # fallback
        else:
            if keep_unknown_fields:

                # якщо число — пробуємо витягнути Decimal
                if isinstance(raw_value, (int, float, Decimal)):
                    value = _safe_decimal(raw_value)
                else:
                    value = _clean_string(raw_value)

            else:
                continue

        # ЗБЕРІГАЄМО ОРИГІНАЛЬНІ НАЗВИ ПОЛІВ
        result[field] = value

    if as_object:
        return SimpleNamespace(**result)

    return result
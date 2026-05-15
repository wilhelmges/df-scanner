from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Optional
import re


# ============================================================================
# Конфігурація полів
# ============================================================================

INT_FIELDS = {
    "PERIOD_M",
    "PERIOD_Y",
    "UKR_GROMAD",
    "ZO",
    "DOG_CPH",
    "VS",
    "PIR",
}

DATE_FIELDS = {
    "START_DT",
    "END_DT",
    "NRM_DT",
}


# ============================================================================
# DTO
# ============================================================================

@dataclass(slots=True)
class PersonRecord:
    PERIOD_M: Optional[int] = None
    PERIOD_Y: Optional[int] = None
    UKR_GROMAD: Optional[int] = None

    NUMIDENT: Optional[str] = None

    LN: Optional[str] = None
    NM: Optional[str] = None
    FTN: Optional[str] = None

    START_DT: Optional[date] = None
    END_DT: Optional[date] = None

    ZO: Optional[int] = None

    PID_ZV: Optional[str] = None

    NRM_DT: Optional[date] = None

    DOG_CPH: Optional[int] = None

    PNR: Optional[str] = None
    PROF: Optional[str] = None
    POS: Optional[str] = None
    PID: Optional[str] = None
    VZV: Optional[str] = None

    VS: Optional[int] = None
    PIR: Optional[int] = None

    OZN: Optional[str] = None


# ============================================================================
# Regex
# ============================================================================

CONTROL_CHARS_RE = re.compile(r"[\x00-\x1F\x7F]")
MULTISPACE_RE = re.compile(r"\s+")

DATE_PATTERNS = (
    "%Y%m%d",
    "%Y-%m-%d",
    "%d.%m.%Y",
    "%d/%m/%Y",
)


# ============================================================================
# Базові helper-функції
# ============================================================================

def safe_str(value: Any, max_len: int | None = None) -> Optional[str]:
    """
    Безпечне очищення строк:
    - None -> None
    - trim
    - видалення control chars
    - нормалізація пробілів
    """

    if value is None:
        return None

    try:
        s = str(value)
    except Exception:
        return None

    s = s.replace("\u00A0", " ")
    s = CONTROL_CHARS_RE.sub("", s)
    s = MULTISPACE_RE.sub(" ", s)

    s = s.strip()

    if not s:
        return None

    if max_len:
        s = s[:max_len]

    return s


def safe_lower(value: Any, max_len: int | None = None) -> Optional[str]:
    s = safe_str(value, max_len=max_len)

    if s is None:
        return None

    return s.lower()


# ============================================================================
# Numeric parser
# ============================================================================

def safe_int(value: Any) -> Optional[int]:
    """
    Толерантний parser int:
    - None
    - ""
    - "1"
    - "1.0"
    - "1,0"
    - " 1 "
    - "1abc"
    """

    if value is None:
        return None

    if isinstance(value, int):
        return value

    try:
        s = str(value)
    except Exception:
        return None

    s = s.strip()

    if not s:
        return None

    s = s.replace("\u00A0", "")
    s = s.replace(" ", "")
    s = s.replace(",", ".")

    s = re.sub(r"[^0-9\-.]", "", s)

    if not s:
        return None

    try:
        return int(float(s))
    except Exception:
        return None


def safe_decimal(value: Any) -> Optional[Decimal]:
    """
    Безпечний Decimal parser.
    """

    if value is None:
        return None

    if isinstance(value, Decimal):
        return value

    try:
        s = str(value)
    except Exception:
        return None

    s = s.strip()

    if not s:
        return None

    s = s.replace("\u00A0", "")
    s = s.replace(" ", "")
    s = s.replace(",", ".")

    s = re.sub(r"[^0-9\-.]", "", s)

    if not s:
        return None

    try:
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return None


# ============================================================================
# Date parser
# ============================================================================

def safe_date(value: Any) -> Optional[date]:
    """
    Підтримує:
    - datetime/date
    - YYYYMMDD
    - YYYY-MM-DD
    - DD.MM.YYYY
    - DD/MM/YYYY
    """

    if value is None:
        return None

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    try:
        s = str(value)
    except Exception:
        return None

    s = s.strip()

    if not s:
        return None

    if s in {
        "00000000",
        "0000-00-00",
        "  /  /    ",
    }:
        return None

    for pattern in DATE_PATTERNS:
        try:
            return datetime.strptime(s, pattern).date()
        except Exception:
            pass

    return None


# ============================================================================
# Спеціальні parser-и
# ============================================================================

def safe_numident(value: Any) -> Optional[str]:
    """
    NUMIDENT:
    - без валідації
    - просто очищена строка
    """

    return safe_lower(value, max_len=10)


def safe_ozn(value: Any) -> str:
    """
    Якщо пусте або сміття -> "-1"
    """

    s = safe_lower(value, max_len=1)

    if s is None:
        return "-1"

    return s


# ============================================================================
# Основна функція
# ============================================================================

def parse_dbf_record(record: Any) -> PersonRecord:
    """
    Приймає:
        dbf.Record або dict-like object

    Повертає:
        PersonRecord

    Максимально толерантна до:
    - битих dbf
    - пустих значень
    - сміття в numeric/date полях
    - control chars
    - неправильних типів
    """

    data: dict[str, Any] = {}

    field_names = [
        "PERIOD_M",
        "PERIOD_Y",
        "UKR_GROMAD",
        "NUMIDENT",
        "LN",
        "NM",
        "FTN",
        "START_DT",
        "END_DT",
        "ZO",
        "PID_ZV",
        "NRM_DT",
        "DOG_CPH",
        "PNR",
        "PROF",
        "POS",
        "PID",
        "VZV",
        "VS",
        "PIR",
        "OZN",
    ]

    # ------------------------------------------------------------------------
    # Безпечне читання полів
    # ------------------------------------------------------------------------

    for field in field_names:

        value = None

        try:
            value = record[field]
        except Exception:
            pass

        if value is None:
            try:
                value = getattr(record, field)
            except Exception:
                pass

        data[field] = value

    # ------------------------------------------------------------------------
    # Формування DTO
    # ------------------------------------------------------------------------

    result = PersonRecord()

    # int fields
    for field in INT_FIELDS:
        setattr(result, field, safe_int(data.get(field)))

    # date fields
    for field in DATE_FIELDS:
        setattr(result, field, safe_date(data.get(field)))

    # strings
    result.NUMIDENT = safe_numident(data.get("NUMIDENT"))

    result.LN = safe_lower(data.get("LN"), max_len=100)
    result.NM = safe_lower(data.get("NM"), max_len=100)
    result.FTN = safe_lower(data.get("FTN"), max_len=100)

    result.PID_ZV = safe_lower(data.get("PID_ZV"), max_len=150)

    result.PNR = safe_lower(data.get("PNR"), max_len=250)
    result.PROF = safe_lower(data.get("PROF"), max_len=6)
    result.POS = safe_lower(data.get("POS"), max_len=250)
    result.PID = safe_lower(data.get("PID"), max_len=250)
    result.VZV = safe_lower(data.get("VZV"), max_len=250)

    result.OZN = safe_ozn(data.get("OZN"))

    return result


# ============================================================================
# Example
# ============================================================================

if __name__ == "__main__":

    fake_record = {
        "PERIOD_M": " 5 ",
        "PERIOD_Y": "2024",
        "UKR_GROMAD": "1",
        "NUMIDENT": " 3124017036 ",
        "LN": " Іваненко\x00 ",
        "NM": " Петро ",
        "FTN": " Іванович ",
        "START_DT": "20240501",
        "END_DT": "00000000",
        "ZO": "51",
        "PID_ZV": " test ",
        "NRM_DT": "01.05.2024",
        "DOG_CPH": "1",
        "PNR": " інженер ",
        "PROF": "123456",
        "POS": " програміст ",
        "PID": None,
        "VZV": "",
        "VS": "1",
        "PIR": "0",
        "OZN": " ",
    }

    rec = parse_dbf_record(fake_record)

    print(rec)
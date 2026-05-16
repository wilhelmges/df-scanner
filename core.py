from pathlib import Path
from datetime import date

def parse_ipn(ipn: str) -> str:
    """
    Повертає строку:
    'Дата народження: 01.01.1990 | Вік: 35 | Стать: чоловіча'
    """

    if not ipn.isdigit() or len(ipn) != 10:
        return "Не ІПН"

    # Перші 5 цифр — кількість днів від 31.12.1899
    days = int(ipn[:5])

    base_date = date(1899, 12, 31)
    birth_date = base_date.fromordinal(base_date.toordinal() + days)

    # Стать:
    # парне передостаннє число -> жіноча
    # непарне -> чоловіча
    gender_digit = int(ipn[8])

    gender = "жінка" if gender_digit % 2 == 0 else "чоловік"

    # Вік
    today = date.today()

    age = (
        today.year
        - birth_date.year
        - (
            (today.month, today.day)
            < (birth_date.month, birth_date.day)
        )
    )

    return (
        f"{gender},"
        f" {age} років, "
        f"ДН: {birth_date.strftime('%d.%m.%Y')}"
    )

def short_dbf_path(path: str) -> str:
    p = Path(path)
    return "\\" + str(Path(*p.parts[-3:]))

def dbf_report_params(filename):
    sway = filename.split("_")[0][-3]
    if sway.isdigit():
        return int(sway)
    return 0 #'cant define for '+filename.split("_")[0]

    # for part in sway[1:]:
    #     if part.isdigit() and int(part) < 13:

def to_int(value, default=-1):
    if value is None:
        return default

    s = str(value).strip()

    if not s:
        return default

    return int(float(s))

def check_tax_code(code: str) -> bool:
    if not code.isdigit():
        return True
    if len(code) != 10:
        return False

    digits = [int(x) for x in code]

    weights = [-1, 5, 7, 9, 4, 6, 10, 5, 7]

    checksum = sum(d * w for d, w in zip(digits[:9], weights))
    checksum %= 11

    if checksum == 10:
        checksum %= 10

    return checksum == digits[9]

# Приклади використання:
# print(check_tax_code("1234567890"))  # Поверне False
# print(check_tax_code("3485012345"))  # Поверне True (якщо контрольна сума збігається)


if __name__ == '__main__':
    print(parse_ipn("3175209377"))
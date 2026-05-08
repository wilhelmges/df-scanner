def dbf_report_params(filename):
    sway = filename.split("_")[0][-3]
    if sway.isdigit():
        return int(sway)
    return 0 #'cant define for '+filename.split("_")[0]

    # for part in sway[1:]:
    #     if part.isdigit() and int(part) < 13:

def check_tax_code(code: str) -> bool:
    if len(code) != 10 or not code.isdigit():
        return False

    weights = [-1, 5, 7, 9, 4, 6, 10, 5, 7]
    digits = list(map(int, code))

    total = sum(d * w for d, w in zip(digits[:9], weights))
    control = total % 11
    if control == 10:
        control = 0

    return control == digits[9]

# Приклади використання:
# print(check_tax_code("1234567890"))  # Поверне False
# print(check_tax_code("3485012345"))  # Поверне True (якщо контрольна сума збігається)


if __name__ == '__main__':
    print(dbf_report_params('J510510_24_9'))
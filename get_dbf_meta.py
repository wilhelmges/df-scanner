import dbf

table = dbf.Table("samples/medok/1 кв. 2026/j0510410_01_2026.dbf", codepage='cp1251')
table.open()
print(table.version)
print(table.structure())

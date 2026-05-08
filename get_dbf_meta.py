import dbf

table = dbf.Table("samples/J0510106_1_23_1.dbf", codepage='cp1251')
table.open()
print(table.version)
print(table.structure())

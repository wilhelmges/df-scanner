from pathlib import Path
from core import dbf_report_params
from grab import grab_df1, check_df1, apply_adjustment

def read_adjustment(filepath):
    table = dbf.Table(str(filepath), codepage='cp1251')
    table.open()

    for record in table:
        print(record.PAY_TP, record.OZN)

def iterate_quarter_folder(str_file_path):
    operations = []
    adjustments = []
    toresearch= []

    file_path = Path(str_file_path)
    for folder in file_path.iterdir():
        if folder.is_dir() and "кв" in folder.name.lower() and "202" in folder.name.lower():
            #print('directory ', folder.name, folder)

            for file in folder.glob("*.dbf"):
                #print(file.stem, dbf_report_params(file.stem))
                if file.stem.lower().startswith("j"):
                    operations.append(file)

            for adjfolder in folder.iterdir():
                if adjfolder.is_dir() and "уточненн" in adjfolder.name.lower():# перевірка без врахування регістру
                    #print("adj folder "+ adjfolder.name)
                    for file in adjfolder.glob("*.dbf"):
                        #print(file.stem, dbf_report_params(file.stem))
                        df_num = dbf_report_params(file.stem)

                        if df_num==1 or df_num==4 or df_num==5:
                            #print("finded DF adjustment " +file.stem)
                            adjustments.append(file)
                        else:
                            #print("cant define ",file.stem)
                            toresearch.append(file)

                    #print("end of folder " + adjfolder.name + '~~~~~~~~~~')
            #print('----------- end of folder '+folder.name)
    return operations, adjustments, toresearch

if __name__=="__main__":
    string_file_path = r"s:\МЕДОК"  #r"C:\progs\df-scanner\samples\short_quarters" #
    #read_adjustment(r"")
    rez = iterate_quarter_folder(string_file_path)
    print(len(rez[0]), len(rez[1]))
    for file in rez[1]:
        #print(file.stem, dbf_report_params(file.stem))
        if dbf_report_params(file.stem)==1:
            apply_adjustment(file)
            # print(str(file))
            #grab_df1(file)

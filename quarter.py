from pathlib import Path
from core import dbf_report_params
from grab import grab_df1, check_df1, apply_df1_adjustment, lookfor23
from file_metadata import FileMetadataStore


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
    string_file_path = r"C:\progs\df-scanner\samples\medok" #r"s:\МЕДОК"  #
    rez = iterate_quarter_folder(string_file_path)
    print(len(rez[0]), len(rez[1]))
    for file in rez[1][:7]:
        if dbf_report_params(file.stem)==1:
            folder = str(file.parent)
            print(folder)
            store = FileMetadataStore(folder)
            if store.is_initialized():
                print("Metadata вже існує")
            else:
                print("Папка ще не ініціалізована")

            print(file.name)
            if not apply_df1_adjustment(file):
                print('failed')
                store.set_status(file.name,"failed"); store.update_file_info(file.name)
            else:
                print('42')
                store.set_status(file.name, "42"); store.update_file_info(file.name)


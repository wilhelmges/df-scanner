from pathlib import Path
from core import dbf_report_params
from grab import grab_df1, apply_df1_adjustment, lookfor23, grab_df4, grab_df5, apply_df5_adjustment, \
    apply_df4_adjustment
from file_metadata import FileMetadataStore
from repository import delete_from_df1, delete_from_df4, delete_from_df5

def iterate_quarter_folder(str_file_path):
    operations = []
    adjustments = []
    toresearch= []

    file_path = Path(str_file_path)
    for folder in file_path.iterdir():
        if folder.is_dir() and "кв" in folder.name.lower() and "202" in folder.name.lower():
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
                        if df_num==1 or df_num==5:
                            adjustments.append(file) #pass
                        elif df_num==4: #df_num==1 or df_num==4 or :
                            #print("finded DF adjustment " +file.stem)
                            pass#adjustments.append(file)
                        else:
                            #print("cant define ",file.stem)
                            toresearch.append(file)

                    #print("end of folder " + adjfolder.name + '~~~~~~~~~~')
            #print('----------- end of folder '+folder.name)
        # else:
        #     print('skip ', folder.name.lower())
    return operations, adjustments, toresearch

if __name__=="__main__":
    string_file_path = r"C:\progs\df-scanner\samples\medok" #r"s:\МЕДОК"  #
    rez = iterate_quarter_folder(string_file_path)

    print(len(rez[0]), len(rez[1]),len(rez[2]))
    print('main data')
    #delete_from_df1(); delete_from_df5();
    delete_from_df4();

    for file in rez[0]:
        df = dbf_report_params(file.stem)
        if df==1:
             pass #grab_df1(file)
        if df==4:
            grab_df4(file) #pass #
        if df==5:
             pass #grab_df5(file)

    print('apply adjustments')
    for file in rez[1]:
        df = dbf_report_params(file.stem)
        if df==1:
            pass# apply_df1_adjustment(file); continue
        if df==4:
            apply_df4_adjustment(file); continue #pass#
        if df == 5:
            pass#apply_df5_adjustment(file); continue
            continue
            lookfor23(file)


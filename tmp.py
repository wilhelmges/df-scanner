from file_metadata import FileMetadataStore

store = FileMetadataStore("samples/medok")
if store.is_initialized():
    print("Metadata вже існує")
else:
    print("Папка ще не ініціалізована")

# store.update_file_info("J0510506_23_1.dbf")
#
# meta = store.get("J0510506_23_1.dbf")
#
# print(meta)
# if "status" in meta:
#     print(meta["status"])
#
# store.set_status("J0510506_23_1.dbf", "processing")
# meta = store.get("J0510506_23_1.dbf")
#
# #store.update_file_info("J0510506_23_1.dbf")
#
# print(meta)
# if "status" in meta:
#     print(meta["status"])
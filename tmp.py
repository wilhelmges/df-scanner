from file_metadata import FileMetadataStore

store = FileMetadataStore("samples/1 кв. 2023")
store.update_file_info("J0510506_23_1.dbf")

meta = store.get("J0510506_23_1.dbf")

print(meta)
if "status" in meta:
    print(meta["status"])

store.set_status("J0510506_23_1.dbf", "processing")
store.update_file_info("J0510506_23_1.dbf")

print(meta)
if "status" in meta:
    print(meta["status"])
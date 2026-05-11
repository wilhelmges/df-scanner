from types import SimpleNamespace

obj = SimpleNamespace(**{
    "field1": 123,
    "field2": "hello"
})

print(obj.field1)  # 123
print(obj)  # hello
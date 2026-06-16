інсталяція пайтон-пакетів з консолі
 pip install -r requirements.txt
якщо не спрацювало, то 
 python -m pip install -r requirements.txt

запуск самого додатку з його папки
 uvicorn main:app --reload

 quarter.py is an entry point to start parsing from dbf-files

 запуск тестів для додатку
 python -m pytest tests/test_routes.py -v
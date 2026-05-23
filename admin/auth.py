from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse

from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend


from db import engine

class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()

        username = form.get("username")
        password = form.get("password")

        # ПРОСТА ПЕРЕВІРКА
        if username == "fesadmin" and password == "D5&095ChEy4s":
            request.session.update({"token": "logged_in"})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if token == "logged_in":
            return True

        return False
from urls import CREATE_USER, LOGIN_USER
import requests
from utilits import delete_user
import pytest
import allure
from data import LOGIN_PARAMETRIZE

class TestLoginUser:
    @allure.feature("Авторизация пользователя")
    @allure.title("Успешная авторизация пользователя")
    def test_login_user_is_success(self, new_user):
        with allure.step("Создание пользователя"):
            token = requests.post(CREATE_USER, json=new_user).json().get("accessToken")
        try:
            with allure.step("Отправка запроса на логин"):
                resp = requests.post(LOGIN_USER, json={"email": new_user["email"], "password": new_user["password"]})
                body = resp.json()
            with allure.step("Проверка успешной авторизации"):
                assert resp.status_code == 200
                assert body.get("success") is True
                assert "accessToken" in body
                assert body.get("user")["email"] == new_user["email"]
        finally:
            delete_user(token)

    @pytest.mark.parametrize("email,password", LOGIN_PARAMETRIZE)
    @allure.feature("Авторизация пользователя")
    @allure.title("Неуспешная авторизация с неверными данными")
    def test_login_invalid_is_not_success(self, new_user, email, password):
        with allure.step("Создание пользователя"):
            token = requests.post(CREATE_USER, json=new_user).json().get("accessToken")
        try:
            with allure.step("Отправка запроса с некорректными данными"):
                resp = requests.post(LOGIN_USER, json={
                    "email": email if "wrong" in email else new_user["email"],
                    "password": password if "wrong" in password else new_user["password"]
                })
                body = resp.json()
            with allure.step("Проверка неуспешной авторизации"):
                assert resp.status_code == 401
                assert body.get("success") is False
                assert body.get("message") == "email or password are incorrect"
        finally:
            delete_user(token)

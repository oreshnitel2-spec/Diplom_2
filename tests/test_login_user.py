from urls import LOGIN_USER
import requests
import pytest
import allure
from data import LOGIN_PARAMETRIZE, MESSAGE_INVALID_LOGIN_DATA

class TestLoginUser:
    @allure.feature("Авторизация пользователя")
    @allure.title("Успешная авторизация пользователя")
    def test_login_user_is_success(self, user_with_token):
        _, _, user_data = user_with_token

        with allure.step("Отправка запроса на логин"):
            resp = requests.post(LOGIN_USER, json={"email": user_data["email"], "password": user_data["password"]})
            body = resp.json()
        with allure.step("Проверка успешной авторизации"):
            assert resp.status_code == 200
            assert body.get("success") is True
            assert "accessToken" in body
            assert body.get("user")["email"] == user_data["email"]


    @pytest.mark.parametrize("email,password", LOGIN_PARAMETRIZE)
    @allure.feature("Авторизация пользователя")
    @allure.title("Неуспешная авторизация с неверными данными")
    def test_login_invalid_is_not_success(self, user_with_token, email, password):
        _, _, user_data = user_with_token

        with allure.step("Отправка запроса с некорректными данными"):
            resp = requests.post(LOGIN_USER, json={
                    "email": email if "wrong" in email else user_data["email"],
                    "password": password if "wrong" in password else user_data["password"]
                })
            body = resp.json()
        with allure.step("Проверка неуспешной авторизации"):
            assert resp.status_code == 401
            assert body.get("success") is False
            assert body.get("message") == MESSAGE_INVALID_LOGIN_DATA

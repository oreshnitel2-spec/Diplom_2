import pytest
from urls import CREATE_USER
import requests
import allure

class TestCreateUser:


    @allure.feature("Создание пользователя")
    @allure.title("Успешное создание нового пользователя")

    def test_create_user_is_sucess(self, user_with_token):
        resp, _ , _ = user_with_token
        body = resp.json()
        with allure.step("Проверка успешного ответа"):
            assert resp.status_code == 200
            assert body.get("success") is True


    @allure.feature("Создание пользователя")
    @allure.title("Нельзя создать уже существующего пользователя")
    def test_create_existing_user_is_forbidden(self, user_with_token):
        _, _, user_data = user_with_token

        with allure.step("Повторная отправка запроса на создание пользователя"):
            resp = requests.post(CREATE_USER, json={
            "email": user_data["email"],
            "password": user_data["password"],  
            "name": user_data["name"]
        })
            body = resp.json()
        with allure.step("Проверка ошибки"):
            assert resp.status_code == 403
            assert body.get("success") is False
            assert body.get("message") == "User already exists"
 
    
    @allure.feature("Создание пользователя")
    @allure.title("Нельзя создать пользователя с пропущенным полем {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, new_user, missing_field):
        user_data = new_user.copy()
        user_data.pop(missing_field)
        with allure.step(f"Отправка запроса без поля: {missing_field}"):
            resp = requests.post(CREATE_USER, json=user_data)
            body = resp.json()
        with allure.step("Проверка ошибки"):
            assert resp.status_code == 403
            assert body.get("success") is False
            assert body.get("message") == "Email, password and name are required fields"
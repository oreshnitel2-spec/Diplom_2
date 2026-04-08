import requests
from urls import CREATE_ORDER
from data import INGREDIENTS, MESSAGE_INVALID_INGREDIENTS
import allure


class TestCreateOrder:

    @allure.feature("Создание заказа")
    @allure.title("Создание заказа с авторизацией и ингридиентами")
    def test_create_order_with_ingredients_and_authorization_is_success(self, user_with_token):
        _, token, _ = user_with_token

        with allure.step("Отправка запроса на создание заказа с авторизацией"):
            resp = requests.post(CREATE_ORDER, json={"ingredients": INGREDIENTS}, headers={"Authorization": token})
            body = resp.json()
        with allure.step("Проверка успешного ответа"):
            assert resp.status_code == 200
            assert body.get("success") is True
            assert "order" in body
    

    @allure.feature("Создание заказа")
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization_is_success(self):
        with allure.step("Отправка запроса на создание заказа без авторизации"):
            resp = requests.post(CREATE_ORDER, json={"ingredients": INGREDIENTS})
            body = resp.json()
        with allure.step("Проверка ответа"):
            assert resp.status_code == 200
            assert body.get("success") is True
            assert "order" in body
    
    @allure.feature("Создание заказа")
    @allure.title("Ошибка при создании заказа без ингредиентов")
    def test_create_order_without_ingredients_is_not_success(self, user_with_token):
        _, token, _ = user_with_token

        with allure.step("Отправка запроса на создание заказа без ингредиентов"):
            resp = requests.post(CREATE_ORDER, json={}, headers={"Authorization": token})
            body = resp.json()
        with allure.step("Проверка ответа"):
            assert resp.status_code == 400
            assert body.get("success") is False
            assert body.get("message") == MESSAGE_INVALID_INGREDIENTS


    @allure.feature("Создание заказа")
    @allure.title("Ошибка сервера при создании заказа с недействительным хэшем ингредиента")
    def test_create_order_with_invalid_ingredient_id_is_not_success(self, user_with_token):
        _, token, _ = user_with_token
        with allure.step("Отправка запроса на создание заказа с недействительным хэшем ингредиента"):
            resp = requests.post(CREATE_ORDER, json={"ingredients": ["invalid_id"]}, headers={"Authorization": token})
        with allure.step("Проверка ответа"):
            assert resp.status_code == 500
        

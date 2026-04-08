import time 
import pytest
from faker import Faker
import allure
from utilits import delete_user
import requests
from urls import CREATE_USER

faker = Faker()
@pytest.fixture
@allure.step("Создание нового пользователя")
def new_user():
    unique_email = f"{int(time.time() * 1000)}_{faker.email()}"
    return {
        "email": unique_email,
        "password": faker.password(length=12),
        "name": faker.first_name()
    }

@pytest.fixture
def user_with_token(new_user):
    with allure.step("Создание пользователя через API"):
        resp = requests.post(CREATE_USER, json=new_user)
        body = resp.json()
        token = body.get("accessToken")
        user_data = new_user

    yield resp, token, user_data

    with allure.step("Удаление пользователя"):
        delete_user(token)
import pytest
from faker import Faker
import allure

faker = Faker()
@pytest.fixture
@allure.step("Создание нового пользователя")
def new_user():
    return {
        "email": faker.email(),
        "password": faker.password(length=12),
        "name": faker.first_name()
    }
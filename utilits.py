import requests
from urls import DELETE_USER
import allure

@allure.step("Удаление пользователя")
def delete_user(token):
    headers = {"Authorization": token}
    requests.delete(DELETE_USER, headers=headers)

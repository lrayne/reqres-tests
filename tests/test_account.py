import requests
from jsonschema import validate
from reqres_tests.schemas.account import (
    register_successfully,
    register_unsuccessfully,
    login_successfully,
    login_unsuccessfully,
)


url = 'https://reqres.in'


def test_register_successfully():

    email = 'eve.holt@reqres.in'
    password = 'pistol'

    endpoint = '/api/register'
    payload = {"email": email, "password": password}
    response = requests.post(url + endpoint, json=payload)
    body = response.json()

    assert response.status_code == 200
    validate(body, schema=register_successfully)


def test_register_unsuccessfully():

    email = 'eve.holt@reqres.in'

    endpoint = '/api/register'
    payload = {"email": email}
    response = requests.post(url + endpoint, json=payload)
    body = response.json()

    assert response.status_code == 400
    validate(body, schema=register_unsuccessfully)


def test_login_successfully():

    email = 'eve.holt@reqres.in'
    password = 'cityslicka'

    endpoint = '/api/login'
    payload = {"email": email, "password": password}
    response = requests.post(url + endpoint, json=payload)
    body = response.json()

    assert response.status_code == 200
    validate(body, schema=login_successfully)


def test_login_unsuccessfully():

    email = 'eve.holt@reqres.in'

    endpoint = '/api/login'
    payload = {"email": email}
    response = requests.post(url + endpoint, json=payload)
    body = response.json()

    assert response.status_code == 400
    validate(body, schema=login_unsuccessfully)

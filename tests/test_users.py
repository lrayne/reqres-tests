import requests
from jsonschema import validate
from reqres_tests.schemas.users import users_list, single_user, create_user, update_user


url = 'https://reqres.in'


def test_all_the_users_should_have_unique_id():

    endpoint = '/api/users'
    response = requests.get(url + endpoint)
    body = response.json()
    ids = [element['id'] for element in body['data']]

    assert response.status_code == 200
    assert body['total'] == 12
    assert list(set(ids)) == ids
    validate(body, schema=users_list)


def test_get_all_the_users_with_delay():

    endpoint = '/api/users?delay=3'
    response = requests.get(url + endpoint)
    body = response.json()

    assert response.status_code == 200
    assert response.elapsed.total_seconds() <= 3.500000
    validate(body, schema=users_list)


def test_get_existing_user_by_id():

    id = '2'

    endpoint = f'/api/users/{id}'
    response = requests.get(url + endpoint)
    body = response.json()

    assert response.status_code == 200
    validate(body, schema=single_user)


def test_get_non_existent_user_by_id():

    id = '23'

    endpoint = f'/api/users/{id}'
    response = requests.get(url + endpoint)
    body = response.json()

    assert response.status_code == 404
    assert body == {}


def test_create_user_successfully():

    name = 'morpheus'
    job = 'leader'

    endpoint = f'/api/users'
    payload = {'name': name, 'job': job}
    response = requests.post(url + endpoint, json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body['name'] == name
    assert body['job'] == job
    validate(body, schema=create_user)


def test_create_user_without_job_successfully():

    name = 'morpheus'

    endpoint = f'/api/users'
    payload = {'name': name}
    response = requests.post(url + endpoint, json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body['name'] == name
    validate(body, schema=create_user)


def test_create_user_without_name_successfully():

    job = 'leader'

    endpoint = f'/api/users'
    payload = {'job': job}
    response = requests.post(url + endpoint, json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body['job'] == job
    validate(body, schema=create_user)


def test_create_user_without_provided_attributes_successfully():

    endpoint = f'/api/users'
    response = requests.post(url + endpoint, json={})
    body = response.json()

    assert response.status_code == 201
    validate(body, schema=create_user)


def test_create_user_with_custom_provided_attribute_successfully():

    value_of_custom_attribute = 'value'

    endpoint = f'/api/users'
    payload = {'myCustomAttribute': value_of_custom_attribute}
    response = requests.post(url + endpoint, json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body['myCustomAttribute'] == value_of_custom_attribute
    validate(body, schema=create_user)


def test_update_user_info():

    name = 'john'
    job = 'co-leader'
    id = '2'

    endpoint = f'/api/users/{id}'
    payload = {'name': name, 'job': job}
    response = requests.put(url + endpoint, json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body['name'] == name
    assert body['job'] == job
    validate(body, schema=update_user)


def test_partial_update_user_info():

    job = 'co-leader'
    id = '2'

    endpoint = f'/api/users/{id}'
    payload = {'job': job}
    response = requests.patch(url + endpoint, json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body['job'] == job
    validate(body, schema=update_user)


def test_delete_user():

    id = '2'
    endpoint = f'/api/users/{id}'

    response = requests.delete(url + endpoint)

    assert response.status_code == 204

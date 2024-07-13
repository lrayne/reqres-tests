import requests
from jsonschema import validate
from reqres_tests.schemas.resources import resources_list, single_resource


url = 'https://reqres.in'


def test_all_the_resources_should_have_unique_id():

    endpoint = '/api/unknown'
    response = requests.get(url + endpoint)
    body = response.json()
    ids = [element['id'] for element in body['data']]

    assert response.status_code == 200
    assert body['total'] == 12
    assert list(set(ids)) == ids
    validate(body, schema=resources_list)


def test_get_existing_resource_by_id():

    id = '2'
    endpoint = f'/api/unknown/{id}'

    response = requests.get(url + endpoint)
    body = response.json()

    assert response.status_code == 200
    assert body['data']['id'] == int(id)
    validate(body, schema=single_resource)


def test_non_existing_resource_by_id():

    id = '23'
    endpoint = f'/api/unknown/{id}'

    response = requests.get(url + endpoint)
    body = response.json()

    assert response.status_code == 404
    assert body == {}

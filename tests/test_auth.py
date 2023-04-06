import requests

END_POINT = 'http://127.0.0.1:5000'


def test_api() -> None:
    url = f'{END_POINT}/api/v1/'
    payload = ''
    response = requests.request('GET', url, data=payload)
    assert response.status_code == 200


def test_register_no_body() -> None:
    url = f'{END_POINT}/api/v1/auth/users/register'
    payload = ''
    headers = {'Authorization': 'Bearer undefined'}
    response = requests.request('POST', url, data=payload, headers=headers)
    assert response.status_code == 400

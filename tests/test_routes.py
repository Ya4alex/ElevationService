import pytest
from shapely.wkt import loads

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here
    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_elevation_pos_1(client):
    response = client.get('/elevation', query_string={
        'wkt': 'POINT(55 160)'
    })
    print(response.json)
    assert response.status_code == 200
    assert loads(response.json['wkt']) == loads('POINT(55 160 770)')


def test_elevation_pos_2(client):
    response = client.get('/elevation', query_string={
        'wkt': 'POINT(56 160)'
    })
    print(response.json)
    assert response.status_code == 200
    assert loads(response.json['wkt']) == loads('POINT(56 160 184)')


def test_elevation_pos_3(client):
    response = client.get('/elevation', query_string={
        'wkt': 'POINT(55 161)'
    })
    print(response.json)
    assert response.status_code == 200
    assert loads(response.json['wkt']) == loads('POINT(55 161 1219)')


def test_elevation_pos_4(client):
    response = client.get('/elevation', query_string={
        'wkt': 'POINT(56 161)'
    })
    print(response.json)
    assert response.status_code == 200
    assert loads(response.json['wkt']) == loads('POINT(56 161 286)')


# -----------------------------------------------------------------------------

def test_elevation_neg_missing_wkt(client):
    response = client.get('/elevation', query_string={})
    assert response.status_code == 400


def test_elevation_neg_invalid_wkt(client):
    response = client.get('/elevation', query_string={
        'wkt': 'INVALID'
    })
    assert response.status_code == 400


def test_elevation_neg_incorrect_wkt(client):
    response = client.get('/elevation', query_string={
        'wkt': 'POINT(1)'
    })
    assert response.status_code == 400


def test_elevation_post_not_allowed(client):
    response = client.post('/elevation')
    assert response.status_code == 405

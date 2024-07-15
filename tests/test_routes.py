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
        'wkt': 'POINT(160 55)'
    })
    print(response.json)
    assert response.status_code == 200
    assert loads(response.json['wkt']) == loads('POINT(160 55 770)')


def test_elevation_pos_2(client):
    response = client.get('/elevation', query_string={
        'wkt': 'POINT(160 56)'
    })
    print(response.json)
    assert response.status_code == 200
    assert loads(response.json['wkt']) == loads('POINT(160 56 184)')


def test_elevation_pos_3(client):
    response = client.get('/elevation', query_string={
        'wkt': 'POINT(161 55)'
    })
    print(response.json)
    assert response.status_code == 200
    assert loads(response.json['wkt']) == loads('POINT(161 55 1219)')


def test_elevation_pos_4(client):
    response = client.get('/elevation', query_string={
        'wkt': 'POINT(161 56)'
    })
    print(response.json)
    assert response.status_code == 200
    assert loads(response.json['wkt']) == loads('POINT(161 56 286)')


def test_elevation_not_in_borders(client):
    response = client.get('/elevation', query_string={
        'wkt': 'POINT(100 50)'
    })
    print(response.json)
    assert response.status_code == 200
    assert loads(response.json['wkt']) == loads('POINT(100 50 -32768)')


def test_elevation_near_the_borders(client):
    response = client.get('/elevation', query_string={
        'wkt': 'POINT(159.999 54.999)'
    })
    print(response.json)
    assert response.status_code == 200
    assert loads(response.json['wkt']) == loads('POINT(159.999 54.999 -32768)')


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


def test_not_found(client):
    response = client.get('/not_found', query_string={})
    assert response.status_code == 404

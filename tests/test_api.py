import pytest
from fee_api import app

@pytest.fixture(scope='module')
def app_():
    app.config.update(
        TESTING=True,
        )
    return app

@pytest.fixture(scope='module')
def client(request, app_):
    return app_.test_client()


def test_fee_get(client):
    response = client.get('/api/v0.1/fee/2750.00/24')
    assert response.status_code == 200


def test_fee_get_loan_not_float(client):
    response = client.get('/api/v0.1/fee/2750/24')
    assert response.status_code == 200

    response = client.get('/api/v0.1/fee/word/24')
    assert response.status_code == 404


def test_fee_get_term_not_int(client):
    response = client.get('/api/v0.1/fee/2750.00/word')
    assert response.status_code == 404


def test_fee_get_loan_out_of_bounds(client):
    response = client.get('/api/v0.1/fee/999.99/12')
    assert response.status_code == 404

    response = client.get('/api/v0.1/fee/20000.01/12')
    assert response.status_code == 404


def test_fee_get_wrong_term(client):
    response = client.get('/api/v0.1/fee/2750/10')
    assert response.status_code == 404


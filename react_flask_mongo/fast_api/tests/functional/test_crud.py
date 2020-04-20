

def test_get(test_client):
    response = test_client.get('/get')
    assert response.status_code == 200'
    assert response.json() == {"to be settled":" . . . "}
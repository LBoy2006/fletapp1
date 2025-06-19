
def test_list_finds(client, db_session):
    resp = client.get('/finds')
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_read_affiliate(client, db_session):
    uid = client.app.state.user_id
    resp = client.get(f'/affiliate/{uid}')
    assert resp.status_code == 200
    assert resp.json()['user_id'] == uid


def test_affiliate_not_found(client, db_session):
    resp = client.get('/affiliate/999')
    assert resp.status_code == 404


def test_request_withdraw(client, db_session):
    uid = client.app.state.user_id
    resp = client.post(f'/affiliate/{uid}/withdraw')
    assert resp.status_code == 200
    assert resp.json()['withdraw_requested'] is True

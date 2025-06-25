
def test_create_membership_payment(client, db_session):
    uid = client.app.state.user_id
    resp = client.post('/payments/membership', json={'user_id': uid, 'months': 3})
    assert resp.status_code == 200
    data = resp.json()
    assert 'payment_url' in data
    assert f"user={uid}" in data['payment_url']
    assert "months=3" in data['payment_url']

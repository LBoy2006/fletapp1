
def test_list_finds(client, db_session):
    resp = client.get('/finds')
    assert resp.status_code == 200
    assert len(resp.json()) == 2

    resp = client.get('/finds', params={'categories1': 'CatA'})
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.get('/finds', params={'categories2': 'BrandY'})
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_find_categories(client, db_session):
    resp = client.get('/finds/categories1')
    assert resp.status_code == 200
    assert set(resp.json()) == {'CatA', 'CatB'}

    resp = client.get('/finds/categories2', params={'categories1': 'CatA'})
    assert resp.status_code == 200
    assert resp.json() == ['BrandX']


def test_toggle_find_favorite(client, db_session):
    uid = client.app.state.user_id
    resp = client.post('/finds/1/favorite', json={'user_id': uid})
    assert resp.status_code == 200
    assert resp.json()['favorite'] is True

    resp2 = client.get('/finds', params={'user_id': uid, 'favorites_only': True})
    assert resp2.status_code == 200
    assert len(resp2.json()) == 1

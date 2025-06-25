
def test_list_finds(client, db_session):
    resp = client.get('/finds')
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    assert all('favorites_count' in f for f in data)
    assert all(f['favorites_count'] == 0 for f in data)



def test_find_categories(client, db_session):
    resp = client.get('/finds/categories')
    assert resp.status_code == 200
    assert set(resp.json()) == {'CatA', 'CatB'}

    resp = client.get('/finds/brands', params={'categories': 'CatA'})
    assert resp.status_code == 200
    assert resp.json() == ['BrandX']


def test_toggle_find_favorite(client, db_session):
    uid = client.app.state.user_id
    resp = client.post('/finds/1/favorite', json={'user_id': uid})
    assert resp.status_code == 200
    assert resp.json()['favorite'] is True

    resp_all = client.get('/finds')
    assert resp_all.status_code == 200
    counts = {f['id']: f['favorites_count'] for f in resp_all.json()}
    assert counts.get(1) == 1

    resp2 = client.get('/finds', params={'user_id': uid, 'favorites_only': True})
    assert resp2.status_code == 200
    assert len(resp2.json()) == 1

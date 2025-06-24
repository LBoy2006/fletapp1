
def test_list_suppliers(client, db_session):
    uid = client.app.state.user_id
    resp = client.get('/suppliers', params={'user_id': uid})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    assert all('favorites_count' in s for s in data)
    assert all(s['favorites_count'] == 0 for s in data)


def test_supplier_categories(client, db_session):
    resp = client.get('/suppliers/categories')
    assert resp.status_code == 200
    assert set(resp.json()) == {'CatA', 'CatB'}


def test_get_supplier(client, db_session):
    resp = client.get('/suppliers/1')
    assert resp.status_code == 200
    assert resp.json()['id'] == 1
    assert resp.json()['categories'] == ['CatA', 'CatB']
    assert resp.json()['favorites_count'] == 0


def test_get_supplier_not_found(client, db_session):
    resp = client.get('/suppliers/999')
    assert resp.status_code == 404


def test_get_supplier_contacts(client, db_session):
    resp = client.get('/suppliers/1/contacts')
    assert resp.status_code == 200
    assert 'contact_link' in resp.json()


def test_toggle_favorite(client, db_session):
    uid = client.app.state.user_id
    resp = client.post('/suppliers/1/favorite', json={'user_id': uid})
    assert resp.status_code == 200
    assert resp.json()['favorite'] is True
    resp_detail = client.get('/suppliers/1')
    assert resp_detail.status_code == 200
    assert resp_detail.json()['favorites_count'] == 1
    # Should now show only one supplier when favorites_only is true
    resp2 = client.get('/suppliers', params={'user_id': uid, 'favorites_only': True})
    assert resp2.status_code == 200
    assert len(resp2.json()) == 1

import httpx

class DummyClient:
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc, tb):
        pass
    async def post(self, url, json=None, headers=None):
        class Resp:
            def json(self_inner):
                return {
                    "id": "inv123",
                    "status": "in-progress",
                    "paymentUrl": "https://pay.example.com/inv123"
                }
        return Resp()


def test_create_payment(client, db_session, monkeypatch):
    monkeypatch.setattr(httpx, 'AsyncClient', lambda: DummyClient())
    uid = client.app.state.user_id
    resp = client.post('/payments', json={'user_id': uid, 'months': 1})
    assert resp.status_code == 200
    data = resp.json()
    assert data['user_id'] == uid
    assert data['months'] == 1
    assert data['payment_url'].startswith('http')

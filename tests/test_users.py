import asyncio
from backend import crud


def test_read_user(client, db_session):
    uid = client.app.state.user_id
    response = client.get(f'/users/{uid}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == uid


def test_read_user_not_found(client, db_session):
    response = client.get('/users/999')
    assert response.status_code == 404


def test_update_user(client, db_session):
    uid = client.app.state.user_id
    response = client.patch(
        f'/users/{uid}',
        json={'agent_number': 'agent', 'location': 'NY'}
    )
    assert response.status_code == 200
    assert response.json()['location'] == 'NY'


def test_pay_membership(client, db_session):
    uid = client.app.state.user_id
    resp = client.post(f'/users/{uid}/pay')
    assert resp.status_code == 200
    assert resp.json()['is_member'] is True


def test_generate_agent_number(client, db_session):
    SessionLocal = client.app.state.SessionLocal

    async def run():
        async with SessionLocal() as db:
            num1 = await crud.generate_agent_number(db)
            await crud.create_user(db, user_id=2, agent_number=num1, telegram_username='user2')
            num2 = await crud.generate_agent_number(db)
            return num1, num2

    num1, num2 = asyncio.get_event_loop().run_until_complete(run())
    assert num1 == 'chn_001'
    assert num2 == 'chn_002'

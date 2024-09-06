import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

from app.main import app, get_session
from app.models import MonsterDetail, MonsterFamily, Item


def test_read_root():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the DQMonsters API. Go to the Swagger UI interface"}

def test_insert_monster(client: TestClient, session: Session):
    """
    - Tests individual insertion of monster data entry into database (MonsterDetail data table)
    """ 
    session.add(MonsterDetail(
        new_name='Slime', 
        old_name='Slime', 
        description='The most abundant of this popular specie', 
        family_id=1
    ))
    session.commit()

    response = client.get('/dqm1/monsters/1')
    data_entry = response.json()
    
    monster_comparison = {
        'id' : 1,
        'new_name' : 'Slime',
        'old_name' : 'Slime',
        'description' : 'The most abundant of this popular specie',
        'family_id' : 1,
        'family' : None,
    }
    
    assert response.status_code == 200
    assert data_entry['new_name'] == monster_comparison['new_name']
    assert data_entry['old_name'] == monster_comparison['old_name']
    assert data_entry['description'] == monster_comparison['description']
    assert data_entry['family_id'] == monster_comparison['family_id']
    assert data_entry == monster_comparison

def test_insert_monster_family(client: TestClient, session: Session):
    """
    Test individual insertion of monster family data into MonsterFamilyBase Model
    """
    family_list = [
        'SLIME',
        'DRAGON',
        'BEAST',
        'BIRD',
        'PLANT',
        'BUG',
        'DEVIL',
        'UNDEAD',
        'MATERIAL',
        '???',
    ]

    for family in family_list:
        session.add(MonsterFamily(family_eng=f'{family}'))
    session.commit()

    for i in range(1,11):
        response = client.get(f'dqm1/family/{i}')
        family_entry = response.json()

        assert response.status_code == 200
        assert family_entry['family_eng'] == family_list[i-1]


def test_insert_item(client: TestClient, session: Session):
    """
    Tests individual insertion of item data into Items table
    """
    session.add(Item(
        item_name='Herb',
        item_category='recovery',
        item_description='Restores around 30 HP',
        price=10,
        sell_price=6,
        sell_location='Bazaar shop 1',
    ))
    session.commit()

    response = client.get('/dqm1/items/1')
    item_entry = response.json()

    item_comparison = {
        'item_name': 'Herb',
        'item_category': 'recovery',
        'item_description': 'Restores around 30 HP',
        'price': 10,
        'sell_price': 6,
        'sell_location': 'Bazaar shop 1',
    }

    assert response.status_code == 200
    for key, value in item_comparison.items():
        assert item_entry[key] == value

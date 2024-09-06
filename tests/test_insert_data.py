import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

from app.main import app, get_session
from app.models import MonsterDetail, MonsterFamily, Item, Skill


def test_read_root():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the DQMonsters API. Go to the Swagger UI interface"}

def test_insert_monster(client: TestClient, session: Session):
    """
    - Tests individual insertion of monster data entry into monsterdetail 
    datatable
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
    Test individual insertion of monster family data into monsterfamily table
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

def test_insert_skill(client: TestClient, session: Session):
    """
    Tests individual insertion of skill data into skill datatable
    Tests association between skills via upgrade_to and upgrade_from
        - 'Blaze' upgrades to 'Blazemore', which upgrades to 'Blazemost'
    """
    session.add(Skill(
        category_type='Attack',
        family_type='Frizz',
        new_name='Frizz',
        old_name='Blaze',
        description='Inflict damage with small fireball ',
        mp_cost=2,
        required_level=2,
        required_mp=7,
        required_intelligence=20,
        upgrade_to_id=2,
    ))
    session.add(Skill(
        category_type='Attack',
        family_type='Frizz',
        new_name='Frizzle',
        old_name='Blazemore',
        description='Inflict damage with giant fireball',
        mp_cost=4,
        required_level=13,
        required_mp=46,
        required_intelligence=64,
        upgrade_to_id=3,
        upgrade_from_id=1,
    ))
    session.add(Skill(
        category_type='Attack',
        family_type='Frizz',
        new_name='Kafrizzle',
        old_name='Blazemost',
        description='Inflict damage with pillars of fire',
        mp_cost=10,
        required_level=28,
        required_mp=112,
        required_intelligence=146,
        upgrade_from_id=2,
    ))
    session.commit()
    
    response = client.get('dqm1/skills/1')
    skill_entry = response.json()

    skill_comparison = {
        "category_type": "Attack",
        "family_type": "Frizz",
        "new_name": "Frizz",
        "old_name": "Blaze",
        "description": "Inflict damage with small fireball ",
        "mp_cost": 2,
        "required_level": 2,
        "required_hp": None,
        "required_mp": 7,
        "required_attack": None,
        "required_defense": None,
        "required_speed": None,
        "required_intelligence": 20,
        "id": 1,
        "upgrade_to": {
            "new_name": "Frizzle",
            "required_hp": None,
            "required_mp": 46,
            "required_attack": None,
            "required_defense": None,
            "required_speed": None,
            "required_intelligence": 64,
            "id": 2,
            "upgrade_to_id": 3,
            "upgrade_from_id": 1,
            "category_type": "Attack",
            "family_type": "Frizz",
            "old_name": "Blazemore",
            "description": "Inflict damage with giant fireball",
            "mp_cost": 4,
            "required_level": 13,
        },
        "upgrade_from": None,
    }
        
    assert response.status_code == 200
    assert skill_entry == skill_comparison
    
    skill_entry_2 = client.get('dqm1/skills/2').json()
    assert response.status_code == 200
    assert skill_entry_2['upgrade_from']['old_name'] == 'Blaze'
    assert skill_entry_2['upgrade_to']['old_name'] == 'Blazemost'


def test_insert_item(client: TestClient, session: Session):
    """
    Tests individual insertion of item data into items datatable
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

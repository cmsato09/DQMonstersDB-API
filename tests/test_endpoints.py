import json
import os
import pytest


def test_read_monsters(client_module, load_all_csvdata):
    """ 
    Test retrieving all monster detail info from database.
    Compare 
    """
    response = client_module.get('dqm1/monsters')
    monster_data = response.json()

    test_data_file_path = os.path.join(os.path.dirname(__file__), 'test_json/test_all_monsters.json')
    with open(test_data_file_path, 'r') as json_file:
        expected_data = json.load(json_file)

    assert response.status_code == 200
    assert monster_data == expected_data


def test_read_monsters_query_family(client_module, load_all_csvdata):
    """ 
    Test retrieving every monster detail info from database by its family_id.
    Retrieving family_id = 2.  
    """
    family_id = 2 # DRAGON family of monsters
    
    response = client_module.get(f'dqm1/monsters?family={family_id}')
    monster_data = response.json()

    test_data_file_path = os.path.join(os.path.dirname(__file__), 'test_json/test_monsters_query_family.json')
    with open(test_data_file_path, 'r') as json_file:
        expected_data = json.load(json_file)

    assert response.status_code == 200
    assert monster_data == expected_data


def test_read_monster(client_module, load_all_csvdata):
    """ 
    Test retrieving monster detail info from database by its monster_id. 
    """
    monsterID = 110
    response = client_module.get(f'dqm1/monsters/{monsterID}')
    monster_entry = response.json()

    monster_comparison = {
        "new_name": "Watabou",
        "old_name": "Watabou",
        "description": "A mischievous mystical creature",
        "family_id": 5,
        "id": 110,
        "family": {
            "family_eng": "PLANT",
            "id": 5
        }
    }

    assert response.status_code == 200
    assert monster_entry == monster_comparison


def test_read_monster_fail(client_module, load_all_csvdata):
    """
    Tests invalid monster_id. Any id value greater than 215 or less than 1 is 
    invalid. 
    """
    monsterID = 999
    response = client_module.get(f'dqm1/monsters/{monsterID}')

    assert response.status_code == 404


def test_read_monsterandskill(client_module, load_all_csvdata):
    """ 
    Tests retrieving monster detail and skill info from database by monster_id.
    """
    monsterID = 110
    response = client_module.get(f'dqm1/monstersandskill/{monsterID}')
    monster_entry = response.json()

    monster_comparison = {
        "new_name": "Watabou",
        "old_name": "Watabou",
        "description": "A mischievous mystical creature",
        "family_id": 5,
        "id": 110,
        "family": {
            "family_eng": "PLANT",
            "id": 5
        },
        "skills": [
            {
            "category_type": "Support",
            "family_type": "Status support",
            "new_name": "Hocus Pocus",
            "old_name": "Chance",
            "description": "Casts a random effect - Can be good or bad",
            "mp_cost": 20,
            "required_level": 40,
            "required_hp": None,
            "required_mp": 224,
            "required_attack": None,
            "required_defense": None,
            "required_speed": None,
            "required_intelligence": 236,
            "id": 120
            },
            {
            "category_type": "Support",
            "family_type": "Map",
            "new_name": "Whistle",
            "old_name": "Whistle",
            "description": "Summons monsters inside the dungeon to fight you",
            "mp_cost": 0,
            "required_level": 4,
            "required_hp": None,
            "required_mp": 28,
            "required_attack": None,
            "required_defense": None,
            "required_speed": None,
            "required_intelligence": 24,
            "id": 152
            },
            {
            "category_type": "Support",
            "family_type": "Status support",
            "new_name": "Follow Suit",
            "old_name": "Imitate",
            "description": "Copy and return every skill cast on Caster for 1 turn",
            "mp_cost": 4,
            "required_level": 21,
            "required_hp": 147,
            "required_mp": 147,
            "required_attack": 126,
            "required_defense": 126,
            "required_speed": 126,
            "required_intelligence": 126,
            "id": 126
            }
        ]
    }

    assert response.status_code == 200
    assert monster_entry == monster_comparison


def test_read_monsterandskill_fail(client_module, load_all_csvdata):
    """ 
    Tests invalid monster_id for monsterandskill endpoint.
    monster_id greater than 215 or less than 1 is invalid.
    """
    monsterID = 999
    response = client_module.get(f'dqm1/monstersandskill/{monsterID}')
    monster_entry = response.json()
    
    assert response.status_code == 404


def test_read_family(client_module, load_all_csvdata):
    """
    Tests family endpoint. Given family_id, returns all monster within family.
    """
    familyID = 4
    response = client_module.get(f'dqm1/family/{familyID}')

    monster_entries = response.json()
    
    test_data_file_path = os.path.join(os.path.dirname(__file__), 'test_json/test_family.json')
    with open(test_data_file_path, 'r') as json_file:
        expected_data = json.load(json_file)

    assert response.status_code == 200
    assert monster_entries == expected_data


def test_read_skills(client_module, load_all_csvdata):
    """
    Tests read_skills endpoint.
    """
    response = client_module.get('dqm1/skills')
    skill_entries = response.json()

    test_data_file_path = os.path.join(os.path.dirname(__file__), 'test_json/test_read_skills.json')
    with open(test_data_file_path, 'r') as json_file:
        expected_data = json.load(json_file)
    
    assert response.status_code == 200
    assert skill_entries == expected_data


def test_read_skills_query_category(client_module, load_all_csvdata):
    """
    Tests read_skills endpoint with category query.
    """
    category = 'Recovery'
    response = client_module.get(f'dqm1/skills?category={category}')
    skill_entries = response.json()

    test_data_file_path = os.path.join(os.path.dirname(__file__), 'test_json/test_read_skills_category_recovery.json')
    with open(test_data_file_path, 'r') as json_file:
        expected_data = json.load(json_file)
    
    assert response.status_code == 200
    assert skill_entries == expected_data


def test_read_skills_query_skillfamily(client_module, load_all_csvdata):
    """
    Tests read_skills endpoint with category query.
    """
    skillfamily = 'Zap'
    response = client_module.get(f'dqm1/skills?skill_family={skillfamily}')
    skill_entries = response.json()

    test_data_file_path = os.path.join(os.path.dirname(__file__), 'test_json/test_read_skills_skillfamily_zap.json')
    with open(test_data_file_path, 'r') as json_file:
        expected_data = json.load(json_file)
    
    assert response.status_code == 200
    assert skill_entries == expected_data
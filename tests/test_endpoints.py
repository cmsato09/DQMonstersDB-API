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
    monster_entry = response.json()

    assert response.status_code == 404

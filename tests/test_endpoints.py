import json
from pathlib import Path


def test_read_monsters(client_module, load_all_csvdata):
    """
    Test retrieving all monster detail info from database.
    Compare
    """
    response = client_module.get("dqm1/monsters")
    monster_data = response.json()

    test_data_file_path = (
        Path(__file__).resolve().parent / "test_json" / "test_all_monsters.json"
    )
    with open(test_data_file_path, "r") as json_file:
        expected_data = json.load(json_file)

    assert response.status_code == 200
    assert monster_data == expected_data


def test_read_monsters_query_family(client_module, load_all_csvdata):
    """
    Test retrieving every monster detail info from database by its family_id.
    Retrieving family_id = 2.
    """
    family_id = 2  # DRAGON family of monsters

    response = client_module.get(f"dqm1/monsters?family={family_id}")
    monster_data = response.json()

    test_data_file_path = (
        Path(__file__).resolve().parent
        / "test_json"
        / "test_monsters_query_family.json"
    )
    with open(test_data_file_path, "r") as json_file:
        expected_data = json.load(json_file)

    assert response.status_code == 200
    assert monster_data == expected_data


def test_read_monster(client_module, load_all_csvdata):
    """
    Test retrieving monster detail info from database by its monster_id.
    """
    monsterID = 110
    response = client_module.get(f"dqm1/monsters/{monsterID}")
    monster_entry = response.json()

    monster_comparison = {
        "new_name": "Watabou",
        "old_name": "Watabou",
        "description": "A mischievous mystical creature",
        "family_id": 5,
        "id": 110,
        "family": {"family_eng": "PLANT", "id": 5},
    }

    assert response.status_code == 200
    assert monster_entry == monster_comparison


def test_read_monster_fail(client_module, load_all_csvdata):
    """
    Tests invalid monster_id. Any id value greater than 215 or less than 1 is
    invalid.
    """
    monsterID = 999
    response = client_module.get(f"dqm1/monsters/{monsterID}")

    assert response.status_code == 404


def test_read_monsterandskill(client_module, load_all_csvdata):
    """
    Tests retrieving monster detail and skill info from database by monster_id.
    """
    monsterID = 110
    response = client_module.get(f"dqm1/monstersandskill/{monsterID}")
    monster_entry = response.json()
    monster_comparison = {
        "new_name": "Watabou",
        "old_name": "Watabou",
        "description": "A mischievous mystical creature",
        "family_id": 5,
        "id": 110,
        "family": {"family_eng": "PLANT", "id": 5},
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
                "id": 120,
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
                "id": 152,
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
                "id": 126,
            },
        ],
    }

    assert response.status_code == 200
    assert monster_entry == monster_comparison


def test_read_monsterandskill_fail(client_module, load_all_csvdata):
    """
    Tests invalid monster_id for monsterandskill endpoint.
    monster_id greater than 215 or less than 1 is invalid.
    """
    monsterID = 999
    response = client_module.get(f"dqm1/monstersandskill/{monsterID}")

    assert response.status_code == 404


def test_read_family(client_module, load_all_csvdata):
    """
    Tests family endpoint. Given family_id, returns all monster within family.
    """
    familyID = 4
    response = client_module.get(f"dqm1/family/{familyID}")

    monster_entries = response.json()

    test_data_file_path = (
        Path(__file__).resolve().parent / "test_json" / "test_family.json"
    )
    with open(test_data_file_path, "r") as json_file:
        expected_data = json.load(json_file)

    assert response.status_code == 200
    assert monster_entries == expected_data


def test_read_family_fail(client_module, load_all_csvdata):
    """
    Tests invalid family_id. Any family_id greater than 10 or less than 1 is invalid
    """
    familyID = 15
    response = client_module.get(f"dqm1/family/{familyID}")

    assert response.status_code == 404


def test_read_skills(client_module, load_all_csvdata):
    """
    Tests read_skills endpoint.
    """
    response = client_module.get("dqm1/skills")
    skill_entries = response.json()

    test_data_file_path = (
        Path(__file__).resolve().parent / "test_json" / "test_read_skills.json"
    )
    with open(test_data_file_path, "r") as json_file:
        expected_data = json.load(json_file)

    assert response.status_code == 200
    assert skill_entries == expected_data


def test_read_skills_query_category(client_module, load_all_csvdata):
    """
    Tests read_skills endpoint with category query.
    """
    category = "Recovery"
    response = client_module.get(f"dqm1/skills?category={category}")
    skill_entries = response.json()

    test_data_file_path = (
        Path(__file__).resolve().parent
        / "test_json"
        / "test_read_skills_category_recovery.json"
    )
    with open(test_data_file_path, "r") as json_file:
        expected_data = json.load(json_file)

    assert response.status_code == 200
    assert skill_entries == expected_data


def test_read_skills_query_skillfamily(client_module, load_all_csvdata):
    """
    Tests read_skills endpoint with category query.
    """
    skillfamily = "Zap"
    response = client_module.get(f"dqm1/skills?skill_family={skillfamily}")
    skill_entries = response.json()

    test_data_file_path = (
        Path(__file__).resolve().parent
        / "test_json"
        / "test_read_skills_skillfamily_zap.json"
    )
    with open(test_data_file_path, "r") as json_file:
        expected_data = json.load(json_file)

    assert response.status_code == 200
    assert skill_entries == expected_data


def test_read_skill(client_module, load_all_csvdata):
    """
    Tests read_skill endpoint. Given skill_id, return individaul skill info.
    """
    skillid = 50
    response = client_module.get(f"dqm1/skills/{skillid}")
    skill_entry = response.json()

    skill_comparison = {
        "id": 50,
        "category_type": "Attack",
        "family_type": "Gigaslash",
        "new_name": "Gigaslash",
        "old_name": "GigaSlash",
        "description": "The most powerful of the sword attacks",
        "mp_cost": 20,
        "required_level": 33,
        "required_hp": 231,
        "required_mp": 164,
        "required_attack": 164,
        "required_defense": None,
        "required_speed": 198,
        "required_intelligence": 198,
        "upgrade_to": None,
        "upgrade_from": None,
    }

    assert response.status_code == 200
    assert skill_entry == skill_comparison


def test_read_skill_fail(client_module, load_all_csvdata):
    """
    Tests read_skill endpoint given invalid skill_id.
    Invalid skill_id is anything greater than 154 or less than 1.
    """
    skillid = 300
    response = client_module.get(f"dqm1/skills/{skillid}")

    assert response.status_code == 404


def test_read_items(client_module, load_all_csvdata):
    """
    Test read_items endpoint. Tests retrieving all item info from database.
    """
    response = client_module.get("dqm1/items")
    item_entries = response.json()

    test_data_file_path = (
        Path(__file__).resolve().parent / "test_json" / "test_read_items.json"
    )
    with open(test_data_file_path, "r") as json_file:
        expected_data = json.load(json_file)

    assert response.status_code == 200
    assert item_entries == expected_data


def test_read_items_query_category(client_module, load_all_csvdata):
    """
    Test read_items endpoint. Tests retrieving all item info from database.
    """
    category = "meat"
    response = client_module.get(f"dqm1/items?category={category}")
    item_entries = response.json()

    items_comparison = [
        {
            "price": 20,
            "item_category": "meat",
            "sell_location": "Bazaar shop 1",
            "id": 5,
            "item_name": "BeefJerky",
            "item_description": "Give to monster to tame during battle or reduce your own monster's WLD (wildness) by 5",
            "sell_price": 15,
        },
        {
            "price": 80,
            "item_category": "meat",
            "sell_location": "Bazaar shop 1",
            "id": 6,
            "item_name": "Porkchop",
            "item_description": "Give to monster to tame during battle or reduce your own monster's WLD (wildness) by 10",
            "sell_price": 60,
        },
        {
            "price": 300,
            "item_category": "meat",
            "sell_location": "Bazaar shop 2",
            "id": 15,
            "item_name": "Rib",
            "item_description": "Give to monster to tame during battle or reduce your own monster's WLD (wildness) by 20",
            "sell_price": 225,
        },
        {
            "price": 1000,
            "item_category": "meat",
            "sell_location": "Bazaar shop 3",
            "id": 17,
            "item_name": "Sirloin",
            "item_description": "Give to monster to tame during battle or reduce your own monster's WLD (wildness) by 100",
            "sell_price": 750,
        },
        {
            "price": None,
            "item_category": "meat",
            "sell_location": "found in field",
            "id": 45,
            "item_name": "BadMeat",
            "item_description": "Give to monster to tame during battle and poisons them. Reduce your own monster's WLD (wildness) by 5 and poisons them",
            "sell_price": None,
        },
    ]

    assert response.status_code == 200
    assert item_entries == items_comparison


def test_read_items_query_selllocation(client_module, load_all_csvdata):
    """
    Test read_items endpoint. Tests retrieving all item info from database.
    """
    selllocation = "Bazaar shop 4"
    response = client_module.get(f"dqm1/items?selllocation={selllocation}")
    item_entries = response.json()

    items_comparison = [
        {
            "price": 5000,
            "item_category": "book",
            "sell_location": "Bazaar shop 4",
            "id": 24,
            "item_name": "QuestBK",
            "item_description": "Makes monster brave. Use multiple times to change personality",
            "sell_price": 3750,
        },
        {
            "price": 5000,
            "item_category": "book",
            "sell_location": "Bazaar shop 4",
            "id": 25,
            "item_name": "HorrorBK",
            "item_description": "Makes monster cowardly. Use multiple times to change personality",
            "sell_price": 3750,
        },
        {
            "price": 5000,
            "item_category": "book",
            "sell_location": "Bazaar shop 4",
            "id": 26,
            "item_name": "BeNiceBK",
            "item_description": "Makes monster gentle. Use multiple times to change personality",
            "sell_price": 3750,
        },
        {
            "price": 5000,
            "item_category": "book",
            "sell_location": "Bazaar shop 4",
            "id": 27,
            "item_name": "CheaterBK",
            "item_description": "Makes monster cold. Use multiple times to change personality",
            "sell_price": 3750,
        },
        {
            "price": 5000,
            "item_category": "book",
            "sell_location": "Bazaar shop 4",
            "id": 28,
            "item_name": "SmartBK",
            "item_description": "Makes monster think hard. Use multiple times to change personality",
            "sell_price": 3750,
        },
        {
            "price": 5000,
            "item_category": "book",
            "sell_location": "Bazaar shop 4",
            "id": 29,
            "item_name": "ComedyBK",
            "item_description": "Makes monster goofy. Use multiple times to change personality",
            "sell_price": 3750,
        },
    ]

    assert response.status_code == 200
    assert item_entries == items_comparison


def test_read_item(client_module, load_all_csvdata):
    """
    Test reading individual item given item_id
    """
    itemID = 3
    response = client_module.get(f"dqm1/items/{itemID}")
    item_entry = response.json()
    item_comparison = {
        "price": 10,
        "item_category": "recovery",
        "sell_location": "Bazaar shop 1",
        "item_description": "Cures poison of one ally",
        "id": 3,
        "item_name": "Antidote",
        "sell_price": 8,
    }

    assert response.status_code == 200
    assert item_entry == item_comparison


def test_read_item_fail(client_module, load_all_csvdata):
    """
    Test reading individual item fail given invalid item_id. Invalid id is
    greater than 47 and less than 1.
    """
    itemID = 50
    response = client_module.get(f"dqm1/items/{itemID}")

    assert response.status_code == 404

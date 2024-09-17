from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import (
    Item,
    MonsterBreedingLink,
    MonsterDetail,
    MonsterFamily,
    MonsterSkillLink,
    Skill,
    SkillCombine,
)


def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": (
            "Welcome to the DQMonsters API. Go to the Swagger UI interface"
        )
    }


def test_insert_monster(client: TestClient, session: Session):
    """
    - Tests individual insertion of monster data entry into monsterdetail
    datatable
    """
    session.add(
        MonsterDetail(
            new_name="Slime",
            old_name="Slime",
            description="The most abundant of this popular specie",
            family_id=1,
        )
    )
    session.commit()

    response = client.get("/dqm1/monsters/1")
    data_entry = response.json()

    monster_comparison = {
        "id": 1,
        "new_name": "Slime",
        "old_name": "Slime",
        "description": "The most abundant of this popular specie",
        "family_id": 1,
        "family": None,
    }

    assert response.status_code == 200
    assert data_entry["new_name"] == monster_comparison["new_name"]
    assert data_entry["old_name"] == monster_comparison["old_name"]
    assert data_entry["description"] == monster_comparison["description"]
    assert data_entry["family_id"] == monster_comparison["family_id"]
    assert data_entry == monster_comparison


def test_insert_monster_family(client: TestClient, session: Session):
    """
    Test individual insertion of monster family data into monsterfamily table
    """
    family_list = [
        "SLIME",
        "DRAGON",
        "BEAST",
        "BIRD",
        "PLANT",
        "BUG",
        "DEVIL",
        "UNDEAD",
        "MATERIAL",
        "???",
    ]

    for family in family_list:
        session.add(MonsterFamily(family_eng=f"{family}"))
    session.commit()

    for i in range(1, 11):
        response = client.get(f"dqm1/family/{i}")
        family_entry = response.json()

        assert response.status_code == 200
        assert family_entry["family_eng"] == family_list[i - 1]


def test_insert_skill(client: TestClient, session: Session):
    """
    Tests individual insertion of skill data into skill datatable
    Tests association between skills via upgrade_to and upgrade_from
        - 'Blaze' upgrades to 'Blazemore', which upgrades to 'Blazemost'
    """
    session.add(
        Skill(
            category_type="Attack",
            family_type="Frizz",
            new_name="Frizz",
            old_name="Blaze",
            description="Inflict damage with small fireball ",
            mp_cost=2,
            required_level=2,
            required_mp=7,
            required_intelligence=20,
            upgrade_to_id=2,
        )
    )
    session.add(
        Skill(
            category_type="Attack",
            family_type="Frizz",
            new_name="Frizzle",
            old_name="Blazemore",
            description="Inflict damage with giant fireball",
            mp_cost=4,
            required_level=13,
            required_mp=46,
            required_intelligence=64,
            upgrade_to_id=3,
            upgrade_from_id=1,
        )
    )
    session.add(
        Skill(
            category_type="Attack",
            family_type="Frizz",
            new_name="Kafrizzle",
            old_name="Blazemost",
            description="Inflict damage with pillars of fire",
            mp_cost=10,
            required_level=28,
            required_mp=112,
            required_intelligence=146,
            upgrade_from_id=2,
        )
    )
    session.commit()

    response = client.get("dqm1/skills/1")
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

    skill_entry_2 = client.get("dqm1/skills/2").json()
    assert response.status_code == 200
    assert skill_entry_2["upgrade_from"]["old_name"] == "Blaze"
    assert skill_entry_2["upgrade_to"]["old_name"] == "Blazemost"


def test_insert_item(client: TestClient, session: Session):
    """
    Tests individual insertion of item data into items datatable
    """
    session.add(
        Item(
            item_name="Herb",
            item_category="recovery",
            item_description="Restores around 30 HP",
            price=10,
            sell_price=6,
            sell_location="Bazaar shop 1",
        )
    )
    session.commit()

    response = client.get("/dqm1/items/1")
    item_entry = response.json()

    item_comparison = {
        "item_name": "Herb",
        "item_category": "recovery",
        "item_description": "Restores around 30 HP",
        "price": 10,
        "sell_price": 6,
        "sell_location": "Bazaar shop 1",
    }

    assert response.status_code == 200
    for key, value in item_comparison.items():
        assert item_entry[key] == value


def test_insert_item_with_none(client: TestClient, session: Session):
    """
    Tests individual insertion of item data into items datatable that has a
    price and sell_price of None
    """
    session.add(
        Item(
            item_name="Tiny medal",
            item_category="dungeon use",
            item_description="Collect and give to medal master for a prize",
            price=None,
            sell_price=None,
            sell_location="found in field",
        )
    )
    session.commit()

    response = client.get("/dqm1/items/1")
    item_entry = response.json()

    item_comparison = {
        "item_name": "Tiny medal",
        "item_category": "dungeon use",
        "item_description": "Collect and give to medal master for a prize",
        "price": None,
        "sell_price": None,
        "sell_location": "found in field",
    }

    assert response.status_code == 200
    for key, value in item_comparison.items():
        assert item_entry[key] == value


def test_monster_skill_link(client: TestClient, session: Session):
    """
    Tests monster datatable association with skill datatable
    """
    session.add(
        MonsterDetail(
            new_name="Slime",
            old_name="Slime",
            description="The most abundant of this popular specie",
            family_id=1,
        )
    )
    session.add(
        Skill(
            category_type="Attack",
            family_type="Sizz",
            new_name="Sizz",
            old_name="Firebal",
            description="Inflict damage to all enemies with a small blaze",
            mp_cost=4,
            required_level=3,
            required_mp=11,
            required_intelligence=23,
        )
    )
    session.add(
        Skill(
            category_type="Attack",
            family_type="Magic Burst",
            new_name="Magic Burst",
            old_name="MegaMagic",
            description="The most powerful spell to affect all enemies",
            mp_cost=999,
            required_level=38,
            required_mp=210,
            required_attack=114,
            required_speed=224,
        )
    )
    session.add(
        Skill(
            category_type="Support",
            family_type="Dazzle",
            new_name="Dazzleflash",
            old_name="Radiant",
            description="Blinds all enemies with its bright light",
            mp_cost=2,
            required_level=12,
            required_mp=42,
            required_speed=72,
            required_intelligence=72,
        )
    )

    session.add(
        MonsterSkillLink(
            monster_id=1,
            skill_id=1,
        )
    )
    session.add(
        MonsterSkillLink(
            monster_id=1,
            skill_id=2,
        )
    )
    session.add(
        MonsterSkillLink(
            monster_id=1,
            skill_id=3,
        )
    )
    session.commit()

    response = client.get("dqm1/monstersandskill/1")
    monster_entry = response.json()

    assert response.status_code == 200
    assert len(monster_entry["skills"]) == 3
    assert monster_entry["skills"][0]["old_name"] == "Firebal"
    assert monster_entry["skills"][1]["old_name"] == "MegaMagic"
    assert monster_entry["skills"][2]["old_name"] == "Radiant"


def test_skill_combine(client: TestClient, session: Session):
    """
    Tests many-to-many connection between skills via SkillCombine Model
    """
    # Add skill to skills datatable.
    session.add(
        Skill(
            # id = 1
            category_type="Attack",
            family_type="Frizz",
            new_name="Frizz",
            old_name="Blaze",
            description="Inflict damage with small fireball ",
            mp_cost=2,
            required_level=2,
            required_mp=7,
            required_intelligence=20,
            upgrade_to_id=2,
        )
    )
    session.add(
        Skill(
            # id = 2
            category_type="Attack",
            family_type="Frizz",
            new_name="Frizzle",
            old_name="Blazemore",
            description="Inflict damage with giant fireball",
            mp_cost=4,
            required_level=13,
            required_mp=46,
            required_intelligence=64,
            upgrade_to_id=3,
            upgrade_from_id=1,
        )
    )
    session.add(
        Skill(
            # id = 3
            category_type="Attack",
            family_type="Frizz",
            new_name="Kafrizzle",
            old_name="Blazemost",
            description="Inflict damage with pillars of fire",
            mp_cost=10,
            required_level=28,
            required_mp=112,
            required_intelligence=146,
            upgrade_from_id=2,
        )
    )
    session.add(
        Skill(
            # id = 4
            category_type="Attack",
            family_type="Frizz",
            new_name="Flame Slash",
            old_name="FireSlash",
            description="Burning blade sword attack",
            mp_cost=3,
            required_level=11,
            required_hp=77,
            required_mp=34,
            required_attack=66,
            required_intelligence=42,
        )
    )
    session.add(
        Skill(
            # id = 5
            category_type="Support",
            family_type="Status support",
            new_name="Muster Strength",
            old_name="ChargeUP",
            description="Additional Damage next turn",
            mp_cost=0,
            required_level=14,
            required_hp=98,
            required_defense=84,
        )
    )

    # Add SkillCombine connection
    # 'FireSlash' can be learned if 'Blazemore' and 'ChargeUP' is known
    session.add(
        SkillCombine(
            combo_skill_id=4,
            needed_skill_id=2,
        )
    )
    session.add(
        SkillCombine(
            combo_skill_id=4,
            needed_skill_id=5,
        )
    )
    session.commit()

    response = client.get("dqm1/skillcombine/4")
    skill_combo = response.json()

    assert response.status_code == 200

    assert skill_combo[0]["needed_skill_id"] == 2
    assert skill_combo[0]["needed_skill"]["old_name"] == "Blazemore"

    assert skill_combo[1]["needed_skill_id"] == 5
    assert skill_combo[1]["needed_skill"]["old_name"] == "ChargeUP"


def test_monster_breeding_link(client: TestClient, session: Session):
    """
    Test breeding combo insertion.
    """
    family_list = [
        "SLIME",  # family id = 1
        "DRAGON",  # family id = 2
        "BEAST",
        "BIRD",
        "PLANT",
        "BUG",
        "DEVIL",
        "UNDEAD",
        "MATERIAL",
        "???",
    ]

    for family in family_list:
        session.add(MonsterFamily(family_eng=f"{family}"))

    session.add(
        MonsterDetail(
            # id = 1
            new_name="Drake Slime",
            old_name="DrakSlime",
            description="Moves & jumps with its tail and wings",
            family_id=1,
        )
    )
    session.add(
        MonsterDetail(
            # id = 2
            new_name="Wild slime",
            old_name="FangSlime",
            description="Has a red Mohawk and is very brave & proud",
            family_id=1,
        )
    )
    session.add(
        MonsterDetail(
            # id = 3
            new_name="Spiked hare",
            old_name="Almiraj",
            description="When cornered, it charges with its sharp horns",
            family_id=3,
        )
    )

    # tests pedigree_family + family2 connection
    session.add(
        MonsterBreedingLink(
            child_id=1,
            pedigree_family_id=1,
            family2_id=2,
        )
    )
    # tests pedigree_family + parent2 connection
    session.add(
        MonsterBreedingLink(
            child_id=2,
            parent2_id=3,
            pedigree_family_id=1,
        )
    )

    session.commit()

    response1 = client.get("dqm1/breeding/1")
    breeding_query1 = response1.json()

    entry_comparison1 = [
        {
            "id": 1,
            "child_id": 1,
            "pedigree_id": None,
            "parent2_id": None,
            "pedigree_family_id": 1,
            "family2_id": 2,
            "child": {
                "id": 1,
                "new_name": "Drake Slime",
                "old_name": "DrakSlime",
                "description": "Moves & jumps with its tail and wings",
                "family_id": 1,
            },
            "pedigree": None,
            "parent2": None,
            "pedigree_family": {
                "family_eng": "SLIME",
                "id": 1,
            },
            "family2": {
                "family_eng": "DRAGON",
                "id": 2,
            },
        },
    ]

    assert response1.status_code == 200
    assert breeding_query1[0]["child_id"] == 1
    assert breeding_query1[0]["child"]["old_name"] == "DrakSlime"
    assert breeding_query1 == entry_comparison1

    response2 = client.get("dqm1/breeding/2")
    breeding_query2 = response2.json()

    entry_comparison2 = [
        {
            "id": 2,
            "child_id": 2,
            "pedigree_id": None,
            "parent2_id": 3,
            "pedigree_family_id": 1,
            "family2_id": None,
            "child": {
                "id": 2,
                "new_name": "Wild slime",
                "old_name": "FangSlime",
                "description": "Has a red Mohawk and is very brave & proud",
                "family_id": 1,
            },
            "pedigree": None,
            "parent2": {
                "id": 3,
                "new_name": "Spiked hare",
                "old_name": "Almiraj",
                "description": (
                    "When cornered, it charges with its sharp horns"
                ),
                "family_id": 3,
            },
            "pedigree_family": {
                "family_eng": "SLIME",
                "id": 1,
            },
            "family2": None,
        }
    ]

    assert response2.status_code == 200
    assert breeding_query2 == entry_comparison2

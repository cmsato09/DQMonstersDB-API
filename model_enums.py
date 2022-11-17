from enum import Enum

"""
ENUMERATE Classes for Swagger UI dropdown menu
https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values
"""


class ItemCategory(str, Enum):
    """
    Creates dropdown menu for read_items() in Swagger UI to filter by
    item_category. Works for predefined choices in item_category.
    For the Item class model
    """
    recovery = "recovery"
    meat = "meat"
    staff = "staff"
    seed = "seed"
    book = "book"
    dungeon_use = "dungeon use"


class ItemSellLocation(str, Enum):
    """
    Creates dropdown menu for read_items() in Swagger UI to filter by
    sell_location. For Item class model
    """
    bazzar_shop_1 = "Bazaar shop 1"
    bazzar_shop_2 = "Bazaar shop 2"
    bazzar_shop_3 = "Bazaar shop 3"
    bazzar_shop_4 = "Bazaar shop 4"
    field_shop = "Field shop"
    found_in_field = "found in field"


class SkillCategory(str, Enum):
    """
    Creates dropdown menu for read_skills() in Swagger UI to filter by
    category_type. Works for predefined choices in the Skill model class
    """
    attack = "Attack"
    support = "Support"
    recovery = "Recovery"


class SkillFamily(str, Enum):
    """
    Creates dropdown menu for read_skills() in Swagger UI to filter by
    family_type. Works for predefined choices in the Skill model class
    """
    frizz = "Frizz"
    sizz = "Sizz"
    bang = "Bang"
    woosh = "Woosh"
    zap = "Zap"
    crack = "Crack"
    whack = "Whack"
    kamikazee = "Kamikazee"
    magic_burst = "Magic Burst"
    help = "Help"
    fire = "Fire"
    ice = "Ice"
    poison = "Poison"
    paralyze = "Paralyze"
    sleep = "Sleep"
    gigaslash = "Gigaslash"
    attack = "Attack"
    dazzle = "Dazzle"
    drain_magic = "Drain Magic"
    fuddle = "Fuddle"
    sap = "Sap"
    curse = "Curse"
    decelerate = "Decelerate"
    ban_dance = "Ban Dance"
    gobstop = "Gobstop"
    lose_turn = "Lose a turn"
    defense = "Defense"
    status_support = "Status support"
    summon = "Summon"
    heal = "Heal"
    status_recovery = "Status recovery"
    revive = "Revive"
    map = "Map"
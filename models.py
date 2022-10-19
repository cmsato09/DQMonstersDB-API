from django.db import models


class BreedingCombo(models.Model):
    """
    Breeding combinations table.
    child_id, pedigree, and parent_2 represent individual monster ids.
    pedigree_family and family_2 represent family type.
    In order to make new monster, two parents are required.
    pedigree determines child
    4 different combinations possible:
    pedigree + parent_2  -- specific monster + specific monster
    pedigree + family_2 -- specific monster + any monster from the family type
    pedigree_family + parent_2 -- specific family type + specific monster
    pedigree_family + family_2 -- family + different family type

    """

    child = models.ForeignKey(
        'MonsterDetail', related_name='breeding_result',
        on_delete=models.DO_NOTHING,
    )
    pedigree = models.ForeignKey(
        'MonsterDetail', null=True, related_name='pedigree_parent',
        blank=True, on_delete=models.DO_NOTHING,
    )
    parent_2 = models.ForeignKey(
        'MonsterDetail', null=True, related_name='parent_partner',
        blank=True, on_delete=models.DO_NOTHING,
    )
    pedigree_family = models.ForeignKey(
        'MonsterFamily', null=True, related_name='pedigree_family',
        blank=True, on_delete=models.DO_NOTHING,
    )
    family_2 = models.ForeignKey(
        'MonsterFamily', null=True, related_name='family_partner',
        blank=True, on_delete=models.DO_NOTHING,
    )


class MonsterDetail(models.Model):
    """
    Monster details from in-game bestiary. Shows name, family, skills, and
    description.
    """

    id = models.IntegerField(null=False, primary_key=True)
    new_name = models.CharField(max_length=30)
    old_name = models.CharField(max_length=30)
    family = models.CharField(max_length=30)
    skill_1 = models.CharField(max_length=30)
    skill_2 = models.CharField(max_length=30)
    skill_3 = models.CharField(max_length=30)
    description = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.old_name}'


class MonsterFamily(models.Model):
    """
    Monster family-type table used as foreign key for the breeding table
    """
    id = models.IntegerField(null=False, primary_key=True)
    family_eng = models.CharField(max_length=10)
    family_jpn = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.family_eng}'

class Item(models.Model):
    """
    Items found in game with description and use.
    """

    item_name = models.CharField(max_length=20)
    item_category = models.CharField(max_length=20)
    item_description = models.CharField(max_length=150)
    price = models.IntegerField(blank=True)
    shop = models.IntegerField(blank=True)
    sell_location = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.item_name}'


class Skill(models.Model):
    """
    Shows description, MP cost, and required stats to learn skill.
    Each monster naturally learns 3 skills.
    """

    category_type = models.CharField(max_length=20)
    skill_family_type = models.CharField(max_length=20)
    new_name = models.CharField(max_length=20)
    old_name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    mp_cost = models.IntegerField(blank=True)
    required_level = models.IntegerField(blank=True)
    required_hp = models.IntegerField(blank=True)
    required_mp = models.IntegerField(blank=True)
    required_attack = models.IntegerField(blank=True)
    required_defense = models.IntegerField(blank=True)
    required_speed = models.IntegerField(blank=True)
    required_intelligence = models.IntegerField(blank=True)

    def __str__(self):
        return f'{self.old_name}'

import csv


def create_skill_dictionary():
    with open('csv_files/practice_skill.csv', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        skill_to_id = {
            row['skill_name'].lower(): row['skill_id'] for row in reader
        }
    return skill_to_id


def create_monster_skill_table():
    with open('csv_files/practice_monster_skill_table.csv',
              encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        monster_skill_table = {
            int(row["id"]): [row["skill_1"].lower(),
                             row["skill_2"].lower(),
                             row["skill_3"].lower()]
            for row in reader
        }
    return monster_skill_table


def main(monster_skill_table, skill_to_id):
    """
    Creates csv file data with monster_id paired with skill_id for
    MonsterSkillLink class model
    Data gathered from two different csv files where one file has a list of
    monster_id that knows a list of skills and a list of skill_id with
    corresponding skill names
    """
    with open('csv_files/DQM1_monster_skill_link.csv', mode='w',
              newline='') as target_file:
        writer = csv.writer(target_file, delimiter=',')
        writer.writerow(['monster_id', 'skill_id'])
        for monster_id, skills in monster_skill_table.items():
            for skill in skills:
                writer.writerow([monster_id, skill_to_id[skill]])


if __name__ == "__main__":
    skill_to_id_dict = create_skill_dictionary()
    monster_skill_dict = create_monster_skill_table()
    main(skill_to_id_dict, monster_skill_dict)

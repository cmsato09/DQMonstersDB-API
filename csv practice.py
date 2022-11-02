import csv

with open('csv_files/practice_skill.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # skips header
    skill_to_id = {row[0].lower(): row[1] for row in reader}

with open('csv_files/practice_monster_skill_table.csv', encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    monster_skill_table = {
        int(row["id"]): [row["skill_1"].lower(),
                         row["skill_2"].lower(),
                         row["skill_3"].lower()]
        for row in reader
    }

with open('csv_files/practice_monster_skill_link.csv', mode='w', newline='') as target_file:
    writer = csv.writer(target_file, delimiter=',')

    writer.writerow(['monster_id', 'skill_id'])
    for monster_id, skills in monster_skill_table.items():
        for skill in skills:
            writer.writerow([monster_id, skill_to_id[skill]])

import csv
import re
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

phone_pattern = re.compile(
    r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:\s*\(?доб\.?\s*(\d+)\)?)?"
)

contact_dict = {}
merge_conflicts = []

for row in contacts_list[1:]:
    fio = " ".join(row[:3]).split()
    fio += [""] * (3 - len(fio))
    new_row = fio[:3] + row[3:]

    phone = new_row[5]
    match = phone_pattern.search(phone)
    if match:
        country, code, part1, part2, part3, ext = match.groups()
        if ext:
            new_row[5] = f"+7({code}){part1}-{part2}-{part3} доб.{ext}"
        else:
            new_row[5] = f"+7({code}){part1}-{part2}-{part3}"

    key = (new_row[0].strip(), new_row[1].strip())

    if key not in contact_dict:
        contact_dict[key] = new_row
    else:
        old_row = contact_dict[key]
        merged = []

        for index, (old_value, new_value) in enumerate(zip(old_row, new_row)):
            if old_value == "" and new_value != "":
                merged.append(new_value)
            else:
                merged.append(old_value)

                if old_value != "" and new_value != "" and old_value != new_value:
                    merge_conflicts.append({
                        "key": key,
                        "column_index": index,
                        "old_value": old_value,
                        "new_value": new_value
                    })

        contact_dict[key] = merged

new_contact_list = [contacts_list[0]] + list(contact_dict.values())

if len(new_contact_list) != 8:
    print(f"Ошибка: итоговое количество строк = {len(new_contact_list)}, ожидалось 8.")
else:
    print("Проверка количества строк пройдена: 8 строк.")

if merge_conflicts:
    print("Обнаружены конфликты при объединении:")
    for conflict in merge_conflicts:
        print(conflict)
else:
    print("Конфликтов при объединении не обнаружено.")

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=",")
    datawriter.writerows(new_contact_list)

pprint(new_contact_list)

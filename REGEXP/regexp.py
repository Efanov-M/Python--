import csv
import re
from pprint import pprint

PHONE_PATTERN = re.compile(
    r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:\s*\(?доб\.?\s*(\d+)\)?)?"
)


def normalize_fio(row):
    fio = " ".join(row[:3]).split()
    fio += [""] * (3 - len(fio))
    return fio[:3] + row[3:]


def normalize_phone(phone):
    if not phone:
        return phone

    match = PHONE_PATTERN.search(phone)
    if not match:
        return phone

    _, code, part1, part2, part3, ext = match.groups()

    if ext:
        return f"+7({code}){part1}-{part2}-{part3} доб.{ext}"
    return f"+7({code}){part1}-{part2}-{part3}"


def can_merge(existing_row, new_row):
    same_lastname = existing_row[0].strip() == new_row[0].strip()
    same_firstname = existing_row[1].strip() == new_row[1].strip()

    if not (same_lastname and same_firstname):
        return False

    existing_surname = existing_row[2].strip()
    new_surname = new_row[2].strip()

    if existing_surname == "" or new_surname == "":
        return True

    return existing_surname == new_surname


def merge_rows(existing_row, new_row, conflicts):
    merged = []

    for column_index, (old_value, new_value) in enumerate(zip(existing_row, new_row)):
        old_value = old_value.strip()
        new_value = new_value.strip()

        if old_value == "" and new_value != "":
            merged.append(new_value)
        else:
            merged.append(old_value)

            if old_value != "" and new_value != "" and old_value != new_value:
                conflicts.append({
                    "lastname": existing_row[0],
                    "firstname": existing_row[1],
                    "surname_existing": existing_row[2],
                    "surname_new": new_row[2],
                    "column_index": column_index,
                    "old_value": old_value,
                    "new_value": new_value,
                })

    return merged


with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list[0]
processed_contacts = []
merge_conflicts = []

for raw_row in contacts_list[1:]:
    new_row = normalize_fio(raw_row)
    new_row[5] = normalize_phone(new_row[5])

    merged_into_existing = False

    for index, existing_row in enumerate(processed_contacts):
        if can_merge(existing_row, new_row):
            processed_contacts[index] = merge_rows(existing_row, new_row, merge_conflicts)
            merged_into_existing = True
            break

    if not merged_into_existing:
        processed_contacts.append(new_row)

new_contact_list = [header] + processed_contacts

if len(new_contact_list) != 8:
    print(f"ПРОВЕРКА НЕ ПРОЙДЕНА: получено {len(new_contact_list)} строк, ожидалось 8.")
else:
    print("ПРОВЕРКА ПРОЙДЕНА: получено 8 строк (заголовок + 7 контактов).")

if merge_conflicts:
    print("\nОбнаружены конфликтующие непустые значения при объединении:")
    for conflict in merge_conflicts:
        print(conflict)
else:
    print("\nКонфликтующих непустых значений не обнаружено.")

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=",")
    datawriter.writerows(new_contact_list)

pprint(new_contact_list)

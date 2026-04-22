from pprint import pprint
import re

import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
#pprint(contacts_list)

contact_dict = {}
index = 1
phone_pattern = re.compile(
    r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:\s*\(?доб\.?\s*(\d+)\)?)?"
    )
while index < len(contacts_list):

    old = contacts_list[index]
    new_row = []
    fio = ' '.join(old[0:3]).split()
    fio += [''] * (3 - len(fio))
    new_row = fio[:3] + old[3:]


    phone = new_row[5]
    match = phone_pattern.search(phone)
    if match:
        country, code, part1, part2, part3, ext = match.groups()
        if ext:
            new_row[5] = f"+7({code}){part1}-{part2}-{part3} доб.{ext}"
        else:
            new_row[5] = f"+7({code}){part1}-{part2}-{part3}"
    key = ' '.join(new_row[0:2])
    if key not in contact_dict:
        contact_dict[key] = new_row
    else:
        merged = []

        for old_value, new_value in zip(contact_dict[key], new_row):

            if old_value == "":

                merged.append(new_value)

            else:

                merged.append(old_value)

        contact_dict[key] = merged

    index += 1

new_contact_list = [contacts_list[0]]+list(contact_dict.values())
#print(new_contact_list)

with open("new_phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')

  datawriter.writerows(new_contact_list)

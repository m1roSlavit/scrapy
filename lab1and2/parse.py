from json import dump
from sqlite3 import connect
from requests import get
import uuid
from re import search
from bs4 import BeautifulSoup

BASE_URL = 'https://lpnu.ua'
page = get(BASE_URL)
soup = BeautifulSoup(page.content, 'html.parser')
connection = connect('res.db')
cursor = connection.cursor()

institutes_array = soup.find(class_='navbar-nav').find(class_='expanded dropdown').find('ul').find_all('a')

tables = ['departments', 'institutes', 'scientists', 'staff']

for i in range(len(tables)):
    cursor.execute(f"DELETE FROM {tables[i]}")

res = []

for inst in institutes_array:
    inst_page = get(BASE_URL + inst.get('href'))
    inst_soup = BeautifulSoup(inst_page.content, 'html.parser')
    directors = inst_soup.find(
        class_='field field--name-field-contact-person field--type-string field--label-hidden field--items').find_all(
        class_='field--item')

    institute = {
        'id': str(uuid.uuid4()),
        'name': inst.getText(),
        'link': BASE_URL + inst.get('href'),
        'staff': [],
        'departments': [],
    }

    cursor.execute(
        "INSERT INTO institutes (name, link, id) VALUES (?, ?, ?)",
        [institute['name'], institute['link'], institute['id']]
    )

    for dir in directors:
        try:
            name = search(r"[А-ЯІЇЄ][а-яіїє']+\s[А-ЯІЇЄ][а-яіїє']+\s[А-ЯІЇЄ][а-яіїє']+", dir.getText()).group(0)
            institute['staff'].append(name)
            cursor.execute(
                "INSERT INTO staff (name, institute_id) VALUES (?, ?)",
                [name, institute['id']]
            )
        except AttributeError:
            institute['staff'].append(dir.getText())
            cursor.execute(
                "INSERT INTO staff (name, institute_id) VALUES (?, ?)",
                [dir.getText(), institute['id']]
            )

    try:
        departments = inst_soup.find(id='block-views-block-group-subgroups-block-1').find(
            class_='item-list').find_all('a')
    except AttributeError:
        continue

    for dep in departments:
        dep_page = get(dep.get('href').strip())
        dep_soup = BeautifulSoup(dep_page.content, 'html.parser')
        dep_arr = dep_soup.find(
            class_="field field--name-field-contact-person field--type-string field--label-hidden field--items").find_all(
            class_="field--item")

        department = {
            'id': str(uuid.uuid4()),
            'name': dep.getText(),
            'link': dep.get('href').strip(),
            'scientists': []
        }

        cursor.execute(
            "INSERT INTO departments (id, name, link, institute_id) VALUES (?, ?, ?, ?)",
            [department['id'], department['name'], department['link'], institute['id']]
        )


        for a in dep_arr:
            try:
                name = search(r"[А-ЯІЇЄ][а-яіїє']+\s[А-ЯІЇЄ][а-яіїє']+\s[А-ЯІЇЄ][а-яіїє']+", a.getText()).group(0)
                department['scientists'].append(name)
                cursor.execute(
                    "INSERT INTO scientists (name, department_id) VALUES (?, ?)",
                    [name, department['id']]
                )
            except AttributeError:
                department['scientists'].append(a.getText())
                cursor.execute(
                    "INSERT INTO scientists (name, department_id) VALUES (?, ?)",
                    [a.getText(), department['id']]
                )

        institute['departments'].append(department)

    res.append(institute)
    connection.commit()

connection.close()

with open('res.json', 'w', encoding='utf-8') as json:
    dump(res, json, ensure_ascii=False, indent=2)

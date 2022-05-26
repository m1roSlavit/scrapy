from re import search

import scrapy
from bs4 import BeautifulSoup
from lab3.items import InstituteItem, StaffItem, ScientistItem, DepartmentItem
from requests import get


class Lab3Spider(scrapy.Spider):
    name = "lab3"
    BASE_URL = "https://lpnu.ua"
    start_urls = ["https://lpnu.ua"]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        institutes_array = soup.find(class_='navbar-nav').find(class_='expanded dropdown').find('ul').find_all('a')
        for inst in institutes_array:
            inst_page = get(self.BASE_URL + inst.get('href'))
            yield InstituteItem(
                name=inst.getText(),
                link=self.BASE_URL + inst.get('href')
            )

            inst_soup = BeautifulSoup(inst_page.content, 'html.parser')
            directors = inst_soup.find(
                class_='field field--name-field-contact-person field--type-string field--label-hidden field--items').find_all(
                class_='field--item')

            for dir in directors:
                try:
                    name = search(r"[А-ЯІЇЄ][а-яіїє']+\s[А-ЯІЇЄ][а-яіїє']+\s[А-ЯІЇЄ][а-яіїє']+", dir.getText()).group(0)
                    yield StaffItem(
                        name=name,
                        institute=inst.getText()
                    )
                except AttributeError:
                    yield StaffItem(
                        name=dir.getText(),
                        institute=inst.getText()
                    )

            try:
                departments = inst_soup.find(id='block-views-block-group-subgroups-block-1').find(
                    class_='item-list').find_all('a')
            except AttributeError:
                continue

            for dep in departments:
                yield DepartmentItem(
                    name=dep.getText(),
                    institute=inst.getText(),
                    link=dep.get('href').strip()
                )
                yield scrapy.Request(
                    url=dep.get('href').strip(),
                    callback=self.parse_departments,
                    meta={
                        'department': dep.getText()
                    }
                )

    def parse_departments(self, responce):
        dep_soup = BeautifulSoup(responce.text, 'html.parser')
        dep_arr = dep_soup.find(
            class_="field field--name-field-contact-person field--type-string field--label-hidden field--items").find_all(
            class_="field--item")

        for a in dep_arr:
            try:
                name = search(r"[А-ЯІЇЄ][а-яіїє']+\s[А-ЯІЇЄ][а-яіїє']+\s[А-ЯІЇЄ][а-яіїє']+", a.getText()).group(0)
                yield ScientistItem(
                    name=name,
                    department=responce.meta["department"]
                )
            except AttributeError:
                yield ScientistItem(
                    name=a.getText(),
                    department=responce.meta["department"]
                )

import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

class Vacancy:

    url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
    list_url = []
    dict_final = {}

    def __init__(self, page):
        self.page = page
        self.headers = Headers(browser='Chrome', os='win').generate()

    def get_urls(self):
        for page in range(self.page):
            url = f'{self.url}&search_field=description&page={page}'
            self.list_url.append(url)

    def get_vacancy_info(self):
        for url in self.list_url:
            response = requests.get(url, headers=self.headers)
            soup_main = BeautifulSoup(response.text, 'html.parser')
            all_tags = soup_main.find_all(class_='serp-item')

            for tag in all_tags:
                title = tag.find(class_='serp-item__title')
                if title.text.count('Django') or title.text.count('Flask'):
                    href = tag.find(class_='serp-item__title').get('href')
                    salary = tag.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
                    salary = 'Договорная' if salary is None else salary.text.replace('\u202f', '')
                    name_company = tag.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text.split()
                    name_company = ' '.join(name_company)
                    city = tag.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]

                    self.dict_final.setdefault(href)
                    self.dict_final[href] = {'salary': salary}
                    self.dict_final[href].update({'name_company': name_company})
                    self.dict_final[href].update({'city': city})

    def write_json(self):
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(self.dict_final, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = Vacancy(10)
    parser.get_urls()
    parser.get_vacancy_info()
    parser.write_json()
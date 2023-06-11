import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

def get_headers():
    return Headers(browser='opera', os='win').generate()


url = 'https://spb.hh.ru/search/vacancy'
params = {
    'area': (1, 2),
    'text': 'python django flask',
    'page': 0,
    'items_on_page': 20
}
parsed_data = []
try:
    while True:
        hh_html = requests.get(url=url, params=params, headers=get_headers()).text
        hh_soup = BeautifulSoup(hh_html, 'lxml')
        print(f'Читаем страницу {params["page"]}')
        params['page'] += 1
        tag_content = hh_soup.find('div', id='a11y-main-content')
        div_item_tags = tag_content.find_all('div', class_='serp-item')

        for div_item_tag in div_item_tags:
            vacancy = div_item_tag.find('h3')
            link = vacancy.find('a').get('href')
            try:
                salary = div_item_tag.find('span', class_='bloko-header-section-3').text.replace('\u202f', '')
            except:
                salary = 'Не указана'
            company = div_item_tag.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', '')
            city = div_item_tag.find('div', class_='vacancy-serp-item__info').contents[1].contents[0]
            parsed_data.append(
                {
                    "вакансия": vacancy.text,
                    "ссылка": link,
                    "зарплата": salary,
                    "название компании": company,
                    "город": city
                }
            )

except:
    print(f'Добавлено {len(parsed_data)} вакансий')

if __name__ == "__main__":
    with open('vacancys.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=5)




# HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
#
# KEYWORDS = ['Django', 'Flask']
#
# def get_headers():
#     pass
# response = requests.get(HOST, headers=get_headers())
# SOURCE = response.text
#
# def get_headers():
#     headers = Headers(browser='opera', os='win')
#     return headers.generate()
# soup = BeautifulSoup(SOURCE, features ='lxml')
#
#
# vacancies = []
#
#
# for article in soup.findAll('article'):
#     link = article.find('a', class_='serp-item_title')['href']
#     salary = article.find('span', class_='bloko-header-section-3').text
#     company = article.find('a', class_='bloko-link bloko-linkkind-tertiary').text
#     city = article.find(class_='bloko-text').text
#
#     vacancies.append({
#              'link': link,
#              'salary': salary,
#              'company': company,
#              'city': city
#              })
#
#     print(vacancies)






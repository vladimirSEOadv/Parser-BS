import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = 'https://minfin.com.ua/'
URL = 'https://minfin.com.ua/cards/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-item')
    cards = []
    for item in items:
        cards.append(
            {
                'title':item.find('div', class_='title').get_text(strip=True),
                'link_product': HOST + item.find('div', class_='title').find('a').get('href'),
                'brand': item.find('div', class_='brand').get_text(strip=True),
                'card_image': HOST + item.find('div', class_='image').find('img').get('src')
            }
        )
    return cards

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название продукта','Ссылка на продукт','Банк','Изображение'])
        for item in items:
            writer.writerow( [item['title'], item['link_product'], item['brand'], item['card_image']])

def parser():
    PAGINATION = input('Укажите количество страниц для парсинга')
    PAGINATION = int(PAGINATION.strip()) + 1 #strip очищает пробелы в вводе пользователя
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGINATION):
            print(f'Парсинг страницы: {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        pass
    else:
        print('Error')

parser()

# get_content(html.text)


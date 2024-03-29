import json
import time
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from data import ENCODING
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def get_page_in_html(path_to_html) -> BeautifulSoup:
    """Получаем страницу BeautifulSoup из файла .html"""
    with open(path_to_html, 'r', encoding=ENCODING) as file:
        index_html = file.read()

    return BeautifulSoup(index_html, 'lxml')


def get_brand(href) -> str:
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver_binary = "/Users/faithk/Documents/pythonProject/geckodriver"
    driver = webdriver.Firefox(executable_path=driver_binary, options=firefox_options)
    try:
        driver.get(href)
        time.sleep(3)
        brand_block = (driver.find_elements(
            By.CLASS_NAME,
            'product-attributes__list-item'
        ))
        time.sleep(3)
        for brand in brand_block:
            text_brand = brand.find_element(By.CLASS_NAME, 'product-attributes__list-item-name-text')
            if text_brand.text.strip() == 'Бренд':
                product_brand = brand.find_element(By.TAG_NAME, 'a').text.strip()
                return product_brand

    except NoSuchElementException:
        print('Ошибка в get_brand()')

    finally:
        driver.close()
        driver.quit()


def parsing(soup: BeautifulSoup) -> list:
    """Создаем словарь из спаршеных данных"""
    id = 1
    i = 1
    elements = (soup.find('div', id='products-inner')
                .find_all('div',
                          class_='catalog-2-level-product-card product-card subcategory-or-type__products-item with-prices-drop'))
    products_available = []

    for el in elements:
        artical_num = el['data-sku']

        # Ссылка на товар
        href = ('https://online.metro-cc.ru' + el.find('a', attrs={'href': True})['href'])

        # Парсим название товара
        name = el.find('span', class_='product-card-name__text').text.strip()
        print(f'{i} - {name}')

        brand = get_brand(href)

        # Цены
        regular_price = (el.find('div', class_='product-unit-prices__actual-wrapper')
                         .find('span', class_='product-price__sum-rubles')).text.strip()
        old_price = (el.find('div', class_='product-unit-prices__old-wrapper')
                     .find('span', class_='product-price__sum-rubles'))
        old_price = (
            'Отсутствует' if old_price is None else old_price.text.strip()
        )

        # Записываем собранные данные в словарь
        products_available.append([{
            'Артикул': artical_num,
            'Ссылка на товар': href,
            'Бренд': brand,
            'Наименование товара': name,
            'Новая цена': regular_price,
            'Старая цена': old_price
        }])
        id += 1
        i += 1

    return list(products_available)


def parse_to_json(data, city):
    """Запись данных в json"""
    with open(f'/Users/faithk/Documents/pythonProject/json_result/{city}/data_{city}.json', 'w', encoding=ENCODING) as file:
        return json.dump(data, file, ensure_ascii=False, indent=4)

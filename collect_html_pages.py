import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from data import CITIES, ENCODING, TIME_DELAY


def get_num_of_pages(driver) -> int:
    """Получаем кол-во страниц с товарами"""
    try:
        try:
            catalog_paginate = driver.find_element(
                By.XPATH,
                '//*[@id="catalog-wrapper"]/main/div[2]/nav/ul'
            ).get_attribute('innerHTML')
        except NoSuchElementException:
            catalog_paginate = driver.find_element(
                By.XPATH,
                '//*[@id="catalog-wrapper"]/main/div[3]/nav/ul'
            ).get_attribute('innerHTML')
        soup = BeautifulSoup(catalog_paginate, 'lxml')
    except Exception as e:
        print('Возникла ошибка в get_num_of_pages()', e)

    return int(soup.find_all('li')[-2].text)


def open_all_pages(driver, num_of_pages, city):
    """Пролистываем все страницы и получаем полный html код"""

    try:
        for i in range(1, num_of_pages + 1):
            if i == num_of_pages:
                with open( f'/Users/faithk/Documents/pythonProject/html_pages/{city}/index_{city}.html', 'w', encoding=ENCODING) as file:
                    file.write(driver.page_source)
                break

            # Находим кнопку "Показать еще"
            try:
                find_more_button = driver.find_element(
                    By.CSS_SELECTOR, '#catalog-wrapper > main > div:nth-child(2) > button > span'
                )
                time.sleep(TIME_DELAY)
            except NoSuchElementException:
                find_more_button = driver.find_element(
                    By.CSS_SELECTOR, '#catalog-wrapper > main > div:nth-child(3) > button > span'
                )

            # Нажимаем на кнопку "Показать еще"
            driver.execute_script("arguments[0].click();", find_more_button)

            time.sleep(TIME_DELAY)
    except Exception as e:
        print('Возникла ошибка в open_all_pages()', e)


def get_city(driver, city_xpath):
    """Получить город на странице"""
    try:
        time.sleep(5)
        change_city = driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div/div[1]/header/div[2]/div[1]/div[2]/button/address'
        )
        change_city.click()
        time.sleep(TIME_DELAY)
        change_delivery = driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div/div[7]/div[2]/div/div[1]/div/div[1]/div/div[2]/div[2]'
        )
        change_delivery.click()
        time.sleep(TIME_DELAY)
        change_button = driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div/div[7]/div[2]/div/div[1]/div/div[1]/div/div[3]/div[1]/span'
        )
        change_button.click()
        choose_city = driver.find_element(By.XPATH, city_xpath)
        choose_city.click()
        time.sleep(TIME_DELAY)
        show_catalog = driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div/div[7]/div[2]/div/div[1]/div/div[1]/div/button'
        )
        show_catalog.click()
        time.sleep(TIME_DELAY)
    except Exception as e:
        print('Возникла ошибка в get_city()', e)



def get_source_html(url: str, city: str) -> None:
    """Получаем полный html код страницы по заданному url"""
    driver_binary = "/Users/faithk/Documents/pythonProject/geckodriver"
    driver = webdriver.Firefox(executable_path=driver_binary)
    driver.maximize_window()

    try:
        driver.get(url=url)
        get_city(driver, CITIES[city])
        open_all_pages(
            driver,
            get_num_of_pages(driver),
            city
        )

    except Exception as e:
        print('Возникла ошибка в get_source_html', e)
    finally:
        driver.close()
        driver.quit()
import requests
from selenium import webdriver
import bs4
import wget
import logging

from config import SCHEDULE_URL, GECKODRIVER_PATH


def get_html(url):
    response = requests.get(url)
    return response.text


def get_html_with_engine(url):
    profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(profile, executable_path=GECKODRIVER_PATH)
    try:
        driver.get(url)
        html = driver.page_source
    except Exception as e:
        logging.info(str(e))
        return
    finally:
        driver.quit()
    return html


def get_link_to_file(url):
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, "lxml")

    div = soup.find("div", class_="visit_link")
    a = div.find("a")

    return a.get("href")


def wget_excel(path):
    try:
        url = get_link_to_file(SCHEDULE_URL)
        wget.download(url, out=path)
    except Exception as e:
        logging.info(str(e))

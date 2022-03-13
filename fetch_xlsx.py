import os
import requests
from selenium import webdriver
import bs4
import wget

from config import SCHEDULE_URL, SCHEDULE_PATH, GECKODRIVER_PATH


def get_html(url):
    response = requests.get(url)
    return response.text


def get_html_with_engine(url):
    profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(profile, executable_path=GECKODRIVER_PATH)
    try:
        driver.get(url)
        html = driver.page_source
    except Exception:
        return None
    finally:
        driver.quit()
    return html


def get_link_to_file(url):
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, "lxml")

    div = soup.find("div", class_="visit_link")
    a = div.find("a")

    return a.get("href")


def wget_excel():
    url = get_link_to_file(SCHEDULE_URL)
    os.remove(SCHEDULE_PATH)
    wget.download(url, out=SCHEDULE_PATH)

import time
import requests
import urllib3

from requests.exceptions import MissingSchema, InvalidSchema, InvalidURL
from selenium import webdriver

from lxml import html


def check_broken_link(link):
    if "teachaway" not in link:
        link = "https://www.teachaway.com" + link

    try:
        request = requests.head(link)
    except requests.exceptions.MissingSchema:
        print("Encountered MissingSchema Exception")
    except requests.exceptions.InvalidSchema:
        print("Encountered InvalidSchema Exception")
    except:
        raise
    else:
        if request.status_code >= 400:
            return False
        else:
            return True

def check_mega_menu_imgs(source):
    imgs_within_main_menu = source.xpath("//ul[contains(@class, 'tb-megamenu-nav')]//img")

    broken_imgs = []

    for img in imgs_within_main_menu:
        try:
            img_src = img.xpath(".//@data-src")[0]
        except IndexError:
            img_src = None

        if img_src and not check_broken_link(img_src):
            broken_imgs.append(img_src)

def check_mega_menu_links(source):
    links_within_main_menu = source.xpath("//ul[contains(@class, 'tb-megamenu-nav')]//a")

    ## if there are exceptions compare with alternatives
    alternative_titles = {
        "UAE": "united-arab-emirates",
        "South Korea": "teach-english-korea",
        "View all online jobs":"online-teaching-jobs",
        "South America": "south-america",
        "South Asia": "south-asia",
        "North America": "usa",
        "The Institute of Applied Technology": "abu-dhabi-vocational-schools/iat",
        "UAE Government Schools": "uae-government-schools",
        "Principal and School Administrator Jobs": "school-administrator-jobs",
        "New York City": "teach-in-nyc",
        "Las Vegas": "teach-in-vegas",
        "Los Angeles": "teach-in-la",
        "Get certified": "certification",
        "Get TEFL certified": "online-tefl-certification",
        "View all jobs": "jobs"

    }

    total_links = 0
    broken_links = []
    incorrect_links = []

    for link in links_within_main_menu:
        try:
            href = link.xpath(".//@href")[0]
        except IndexError:
            href = ""

        try:
            text = link.xpath(".//text()")[0]
        except IndexError:
            text = ""

        if href:
            total_links += 1

            if not check_broken_link(href):
                broken_links.append(href)

        ## Check if text exists in link
        if text and href:

            try:
                first_part = text.split()[0]
            except IndexError:
                pass
            else:
                if alternative_titles.get(text, None):
                    first_part = alternative_titles[text]

                if first_part.lower() not in href:
                    incorrect_links.append([text, href])

def main():
    # Give the location of the file
    options = webdriver.ChromeOptions()

    ## Disable extensions for faster load
    options.add_argument("--disable-extensions")

    ## Disable javascript for faster load
    options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})

    driver = webdriver.Chrome(
        options=options,
        executable_path=r"C:/Users/User/Desktop/selenium/chromedriver.exe",
    )

    # open the url
    driver.get("https://www.teachaway.com/")
    source_soup = html.fromstring(driver.page_source)

    ## Check links and imgs
    check_mega_menu_links(source_soup)
    check_mega_menu_imgs(source_soup)

    driver.quit()

if __name__ == "__main__":
    main()

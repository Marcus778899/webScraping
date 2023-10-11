from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from time import sleep
import information


def open_url():
    option = webdriver.ChromeOptions()
    option.add_argument("start-maximized")
    option.add_argument("disable-infobars")
    option.add_argument("--disable-extensions")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--no-sandbox")
    option.add_argument("--incognito")
    option.add_argument("--disable-popup-blocking")
    option.add_argument("--disable-notifications")
    option.add_argument("--lang=zh-TW")

    service = Service("./chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=option)
    driver.get("https://twitter.com/login")

    return driver


def login(driver):
    email = information.email
    password = information.password
    username = information.username
    try:
        login_email = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input"))
        )

        # 輸入帳號
        login_email.send_keys(email)
        sleep(1)
        login_email.send_keys(Keys.ENTER)
        sleep(1)

        # 確認使用者身分
        try:
            check_user = driver.find_element(By.ID, "modal-header")
            if (
                check_user.text == "Enter your phone number or username"
                or check_user.text == "輸入你的電話號碼或使用者名稱"
            ):
                check_username = driver.find_element(By.CSS_SELECTOR, "input")
                check_username.send_keys(username)
                check_username.send_keys(Keys.ENTER)
                sleep(2)
        except:
            pass

        # 輸入密碼
        login_password = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'password']"))
        )
        login_password.send_keys(password)
        sleep(1)
        login_password.send_keys(Keys.ENTER)
        sleep(1)

    except TimeoutException:
        print("登入失敗")


def scroll(driver):
    total_height = 0
    scroll_height = 300
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span"))
    )
    while total_height < 6000:
        total_height += scroll_height
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")


def search(keyword):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input"))
        )
        input_search = driver.find_element(
            By.CSS_SELECTOR, "div.css-1dbjc4n.r-16y2uox.r-1wbh5a2 input.r-30o5oe"
        )
        input_search.send_keys(keyword)
        input_search.send_keys(Keys.ENTER)
        sleep(1)
    except TimeoutException:
        print("搜尋失敗")


def scraping_data():
    all_post = driver.find_elements(By.CSS_SELECTOR, "article.css-1dbjc4n")
    for post in all_post:
        print(post)
        print("=" * 50)
        sleep(1)


if __name__ == "__main__":
    driver = open_url()
    login(driver)
    sleep(5)
    search("美食")
    scroll(driver)
    scraping_data()
    driver.close()

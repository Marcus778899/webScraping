from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


def get_driver():
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
    driver.get("https://www.104.com.tw/jobs/main/")

    return driver


def search_job(job):
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.form-control"))
    )
    search_bar = driver.find_element(By.CSS_SELECTOR, "input.form-control")
    search_bar.send_keys(job)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(1)


def scroll():
    total_height = 0
    scroll_height = 300
    while total_height < 6000:
        total_height += scroll_height
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.js-job-link"))
        )
        driver.execute_script(f"window.scrollTo(0, {total_height});")
    time.sleep(1)


def job_list(job):
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.job-list-item__info"))
    )
    job_data = []
    job_list = driver.find_elements(
        By.CSS_SELECTOR,
        "article.b-block--top-bord.job-list-item.b-clearfix.js-job-item ",
    )
    for i, item in enumerate(job_list):
        job_info = item.text.split("\n")
        title = job_info[0]
        company = job_info[1]
        category = job_info[2]
        location = job_info[3]
        experience = job_info[4]
        education = job_info[5]
        description = job_info[6:]
        job_data.append(
            {
                "Title": title,
                "Company": company,
                "Category": category,
                "Location": location,
                "Experience": experience,
                "Education": education,
                "Description": " ".join(description),
            }
        )
        print(f"第{i}筆資料完成")

    df = pd.DataFrame(job_data)
    df.to_csv(f"./jobsearch/{job}.csv", index=False)


if __name__ == "__main__":
    driver = get_driver()
    job = "python"
    search_job(job)
    scroll()
    job_list(job)
    driver.close()

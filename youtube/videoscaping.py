from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from time import sleep
import json
import os

my_options = webdriver.ChromeOptions()
my_options.add_argument("--start-maximized")
my_options.add_argument("--incognito")
my_options.add_argument("--disable-popup-blocking")
my_options.add_argument("--disable-notifications")
my_options.add_argument("--lang=zh-TW")

folderPath = "./youtube/scraping"
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

my_service = Service(executable_path=".chromedriver.exe")
driver = webdriver.Chrome(options=my_options, service=my_service)


listData = []


def visit():
    driver.get("https://www.youtube.com/")


def search():
    txtInupt = driver.find_element(By.CSS_SELECTOR, "input#search")
    txtInupt.send_keys("daniel powter")

    sleep(1)

    txtInupt.submit()

    sleep(1)


# 篩選
def filterFunc():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "ytd-toggle-button-renderer.style-scope.ytd-search-sub-menu-renderer",
                )
            )
        )
        # 篩選器
        driver.find_element(
            By.CSS_SELECTOR,
            "ytd-toggle-button-renderer.style-scope.ytd-search-sub-menu-renderer",
        ).click()

        sleep(2)

        driver.find_elements(
            By.CSS_SELECTOR,
            "a#endpoint.yt-simple-endpoint.style-scope.ytd-search-filter-renderer",
        )[9].click()

        sleep(2)

    except TimeoutException:
        print("連線逾時")


# 滾到捲軸
def scroll():
    """
    innerHeight => 瀏覽器內部的高度
    offset => 當前捲動的量(高度)
    count => 累計無效滾動次數
    limit => 最大無效滾動次數
    """
    innerHeight = 0
    offset = 0
    count = 0
    limit = 3

    # 在捲動到沒有元素動態產生前，持續捲動
    while count <= limit:
        # 每次移動高度
        offset = driver.execute_script("return document.documentElement.scrollHeight;")
        """
        或是每次只滾動一點距離，
        以免有些網站會在移動長距離後，
        將先前移動當中的元素隱藏

        例如將上方的 script 改成:
        offset += 600
        """
        # 捲軸往下滾
        driver.execute_script(
            f"""
            window.scrollTo({{
                top :{offset},
                behavior: 'smooth'
            }})
        """
        )

        """
        [補充]
        如果要滾動的是 div 裡面的捲軸，可以使用以下的方法
        document.querySelector('div').scrollTo({...})
        """
        # (重要)強制等待，此時若有新元素生成，瀏覽器內部高度會自動增加
        sleep(3)

        innerHeight = driver.execute_script(
            "return document.documentElement.scrollHeight;"
        )

        # 經過計算，如果滾動距離(offset)大於等於視窗內部總高度(innerHeight)，代表已經到底了
        if offset == innerHeight:
            count += 1

        # 為了實驗功能，捲動超過一定的距離，就結束程式
        if offset >= 600:
            break


# 分析頁面元素資訊
def parse():
    # 使用全域變數(加上後面的clear可以更好的除parse的bug)
    global listData

    # 清空存放資料的變數
    listData.clear()

    elements = driver.find_elements(
        By.CSS_SELECTOR, "ytd-video-renderer.style-scope.ytd-item-section-renderer"
    )

    for elm in elements:
        print("=" * 30)

        # 取得圖片連結
        img = elm.find_element(By.CSS_SELECTOR, "a#thumbnail img")

        imgSrc = img.get_attribute("src")
        print(imgSrc)

        # 取得資料名稱
        a = elm.find_element(By.CSS_SELECTOR, "a#video-title")
        aTitle = a.get_attribute("innerText")
        print(aTitle)

        # 取得連結
        aLink = a.get_attribute("href")
        print(aLink)

        # 取得影音ID(shorts以及v=後面截掉)
        strDelimiter = ""
        if "shorts" in aLink:
            strDelimiter = "/shorts/"
        else:
            strDelimiter = "v="
        youtube_id = aLink.split(strDelimiter)[1]
        youtube_id = youtube_id.split("&")[0]
        print(youtube_id)

        # 放資料到 list 中
        listData.append(
            {"id": youtube_id, "title": aTitle, "link": aLink, "img": imgSrc}
        )


# 將list存成json
def saveJson():
    with open(f"{folderPath}/youtube.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(listData, ensure_ascii=False, indent=4))


def close():
    driver.close()


if __name__ == "__main__":
    visit()
    search()
    filterFunc()
    scroll()
    parse()
    saveJson()
    close()

# FB爬蟲


def openFB(url):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service

    my_options = webdriver.ChromeOptions()
    my_options.add_argument("--start-maximized")  # 最大化視窗
    my_options.add_argument("--incognito")  # 開啟無痕模式
    my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
    my_options.add_argument("--disable-notifications")  # 取消 chrome 推播通知
    my_options.add_argument("--lang=zh-TW")  # 設定為正體中文

    my_service = Service(executable_path="../chromedriver.exe")
    driver = webdriver.Chrome(options=my_options, service=my_service)
    driver.get(url)
    return driver


def loginFB(username, password, driver):
    import time
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))
    )
    login = driver.find_element(By.ID, "email")
    login.send_keys(username)

    password_field = driver.find_element(By.ID, "pass")
    password_field.send_keys(password)
    login.send_keys(Keys.RETURN)
    time.sleep(5)

    locked_account_elements = driver.find_elements(
        By.XPATH, '//*[contains(text(),"你的帳號暫時被鎖住")]'
    )
    if len(locked_account_elements) > 0:
        print("Re-login")
        confirm_buttons = driver.find_elements(By.XPATH, '//*[contains(text(),"是")]')
        if len(confirm_buttons) >= 2:
            confirm_buttons[1].click()


def scroll():
    import time

    innerHeight = 0
    offset = 0
    count = 0
    limit = 3
    while count <= limit:
        offset = driver.execute_script("return document.documentElement.scrollHeight;")
        driver.execute_script(
            f"""
            window.scrollTo({{
                top: {offset}, 
                behavior: 'smooth' 
            }});
        """
        )
        time.sleep(3)
        innerHeight = driver.execute_script(
            "return document.documentElement.scrollHeight;"
        )

        if offset == innerHeight:
            count += 1

        if offset >= 600:
            break


def traffic_information(driver):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    import time

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.xtlvy1s.x126k92a")
        )
    )
    # 發文者
    target_guy = driver.find_elements(
        By.CSS_SELECTOR,
        "div.x1cy8zhl.x78zum5.x1q0g3np.xod5an3.x1pi30zi.x1swvt13.xz9dl7a span",
    )
    # 標籤
    target_tag = driver.find_elements(
        By.CSS_SELECTOR, "div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a"
    )
    # 內容
    tag = "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f"
    tag = tag.replace(" ", ".")
    target_content = driver.find_elements(
        By.CSS_SELECTOR,
        "div.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.xtlvy1s.x126k92a ",
    )
    n = 0
    while True:
        try:
            driver.execute_script(f'document.querySelector("div.{tag}").click();')
            time.sleep(2)
            n += 1
        except:
            break
        if n >= 10:
            break
    soup = {}
    for guy, tag, content in zip(target_guy, target_tag, target_content):
        guy_text = guy.text
        tag_text = tag.text
        content_text = content.text
        soup[guy_text] = (tag_text, content_text)

    return soup


if __name__ == "__main__":
    url = "https://www.facebook.com"
    driver = openFB(url)

    from information import *

    username = username
    password = password

    loginFB(username, password, driver)
    groups = "https://www.facebook.com/groups/TaiwanSurfCarpool"
    driver.get(groups)
    scroll()
    soup = traffic_information(driver)
    for index, (person, content) in enumerate(soup.items()):
        print(f"第{index+1}筆資料:\n{person}\n{content}")
        print("=" * 50)
    driver.close()

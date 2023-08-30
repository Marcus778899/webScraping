import requests as req
from bs4 import BeautifulSoup as bs
import os
import json

folderPath = "linesticker"
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

line = []


url = "https://store.line.me/stickershop/product/23051922/zh-Hant"

res = req.get(url)
soup = bs(res.text, "lxml")
li_elements = soup.select("li.mdCMN09Li.FnStickerPreviewItem.static-sticker ")


for i in li_elements:
    strJson = i["data-preview"]
    obj = json.loads(strJson)
    line.append(obj)

print(line[0])
for obj in line:
    os.system(f'curl {obj["staticUrl"]} -o {folderPath}/{obj["id"]}.jpg')
    print(f'{obj["id"]}下載連結:{obj["staticUrl"]}')

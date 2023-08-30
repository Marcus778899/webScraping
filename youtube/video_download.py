import os
import wget
import json
import subprocess

folderPath = "./youtube/scraping"


def download():
    # 確認yt-dlp是否存在
    if not os.path.exists("./yt-dlp.exe"):
        print("[下載yt-dlp]")
        wget.download(
            "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe",
            "./yt-dlp.exe",
        )

    with open(f"{folderPath}/youtube.json", "r", encoding="utf-8") as file:
        # 取得json字串
        strJson = file.read()
    # 將json轉成list(這樣城市才可以讀取)
    listResult = json.loads(strJson)

    # 下載檔案
    for index, obj in enumerate(listResult):
        if index == 3:
            break

        print(f"正在下載:{obj['link']}")

        # 定義指令
        cmd = [
            "./yt-dlp.exe",
            obj["link"],
            "-f",
            "b[ext=mp4]",
            "-o",
            f"{folderPath}/%(id)s.%(ext)s",
        ]

        # 執行指令，並取得回傳結果 (subprocess 物件)
        obj_sp = subprocess.run(cmd)

        """
        obj_sp 物件的內容:
        
        CompletedProcess(
            args=[
                './yt-dlp.exe', 
                'https://www.youtube.com/watch?v=XHCBKSI1ppM&pp=ygUJ5by15a245Y-L', 
                '-f', 
                'b[ext=mp4]', 
                '-o',
                'youtube/%(id)s.%(ext)s'
            ], 
            returncode=0
        )
        """
        # 判斷指令行是否正常 (returncode == 0 代表正常)
        if obj_sp.returncode == 0:
            print("下載成功")
        else:
            print("下載失敗")

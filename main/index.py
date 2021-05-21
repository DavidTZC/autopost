# coding=utf-8
import json
import random
import os
import main
import time
import sign
import requests
from shutil import rmtree as remove
print("开始 " + time.strftime("%Y/%m/%d") + " 的打卡任务\n")
files = open(os.getcwd() + "/main/day.txt", 'r+')
if files.read() == time.strftime("%Y/%m/%d"):
    print("今日已打卡")
    if os.path.exists(os.getcwd() + "/main/__pycache__/"):
        remove(os.getcwd() + "/main/__pycache__/")

def wechat(text, desp):
    return requests.get(
        "https://sc.ftqq.com/SCU164225T52e7796539ad296f29e329de86a417f46046e3310caaf.send?text=" + text + "&desp=" + desp).json()
    
try:
    wechat("开始 " + time.strftime("%Y/%m/%d") + " 自动打卡任务","[点我查看运行状况](https://github.com/xsk666/autopost/actions)")
except RuntimeError:
    print("推送微信通知出错")


# 读取用户列表
f2 = open(os.getcwd() + "/main/users.json", 'r', encoding='utf-8')
info = json.loads(f2.read())
f2.close()
for i in range(0, len(info)):
    if info[i].get("enable") == 'true':
        print("开始为 " + info[i].get("name") + " 打卡...")
        # 随机UA
        f = open(os.getcwd() + "/main/ua.txt", 'r', encoding='utf-8')
        num = f.read().split("\n")
        UA = num[random.randint(0, len(num) - 1)]
        f.close()
        try:
            # 获取用户cookie
            cook = sign.login(info[i], UA)
            main.run(info[i], UA, cook)
        except Exception:
            print("---为 " + info[i].get("name") + " 打卡失败\n")

print("打卡结束")
# 回到文件头部，清除重写
files.seek(0)
files.truncate()
files.write(time.strftime("%Y/%m/%d"))
files.close()
if os.path.exists(os.getcwd() + "/main/__pycache__/"):
    remove(os.getcwd() + "/main/__pycache__/")

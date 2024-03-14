from pathlib import Path
import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


# import pandas as pd


def get_script_dir():
    """Get the directory where the current Python script is located."""
    if "__file__" in globals():
        script_path = Path(os.path.abspath(__file__)).resolve().parent
    else:
        script_path = Path.cwd()
    return script_path


def create_directory_if_not_exists(directory):
    """Check if the directory exists; create it if it doesn't."""
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)


def get_submittable_meeting():
    url = "http://www.yixuehuiyi.net/xueshuhuiyi/list_1.html"
    # 发起 HTTP GET 请求
    response = requests.get(url)

    # 解析 HTML 内容
    data_international = []
    data_domestic = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # 提取所有<li>标签
        li_tags = soup.find_all("li")

        # 遍历<li>标签，并提取标题、链接、时间和地点
        for li in li_tags:
            span_tag = li.find("span")
            if span_tag is None:
                continue
            time_location = span_tag.text.strip()
            time, location = time_location.split(" ", 2)[:2]
            a_tag = li.find("a")
            title = a_tag.text.strip()
            link = a_tag["href"]

            # 判断地点是否在 cities and provinces.txt 中
            try:
                with open(get_script_dir() / "cities and provinces.txt", "r") as file:
                    cities_and_provinces = file.read().splitlines()
            except FileNotFoundError:
                print("cities and provinces.txt not found.")
                exit()
            if location in cities_and_provinces:
                data_domestic.append([title, time, location, link])
            else:
                data_international.append([title, time, location, link])

    # 添加当天时间并保存成 json 格式
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_data = {
        "domestic": data_domestic,
        "international": data_international,
        "date": current_date,
    }
    return output_data


if __name__ == "__main__":
    output_data = get_submittable_meeting()
    with open("meeting_data.json", "w") as outfile:
        json.dump(output_data, outfile, indent=4, ensure_ascii=False)

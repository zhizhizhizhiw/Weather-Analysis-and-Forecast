import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.tianqihoubao.com/lishi/dalian/month/{year}{month:02d}.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

all_data = []

for year in range(2022, 2026):  # ✅ 包含2025年1-6月
    for month in range(1, 13):
        if year == 2025 and month > 6:
            continue  # ✅ 只爬取2025年1-6月
        url = base_url.format(year=year, month=month)
        print(f"正在爬取: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")

            table = soup.find("table", class_="weather-table")
            if table is None:
                print(f"⚠️ 无数据: {url}")
                continue

            rows = table.find("tbody").find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 4:
                    continue
                date = cols[0].get_text(strip=True)
                weather = cols[1].get_text(strip=True)
                temp = cols[2].get_text(strip=True)
                wind = cols[3].get_text(strip=True)

                all_data.append({
                    "date": date,
                    "weather": weather,
                    "temp": temp,
                    "wind": wind,
                    "year": year,
                    "month": month
                })
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ 失败: {url}, 错误: {e}")
            continue

# ✅ 保存原始数据
df = pd.DataFrame(all_data)
df.to_csv("dalian_weather.csv", index=False, encoding="utf-8")
print("✅ 爬取完成，总行数:", len(df))

# ✅ 清洗数据
df = pd.read_csv("dalian_weather.csv")

# 拆分白天/夜晚风力
df[["wind_day", "wind_night"]] = df["wind"].str.split('/', expand=True)
df["wind_day_level"] = df["wind_day"].str.extract(r'(\d+-\d+)')
df["wind_night_level"] = df["wind_night"].str.extract(r'(\d+-\d+)')

# 拆分温度
df[["temp_high", "temp_low"]] = df["temp"].str.extract(r'(-?\d+)℃/(-?\d+)℃')
df["temp_high"] = pd.to_numeric(df["temp_high"], errors="coerce")
df["temp_low"] = pd.to_numeric(df["temp_low"], errors="coerce")

# 拆分白天/夜晚天气
df[["weather_day", "weather_night"]] = df["weather"].str.split('/', expand=True)

# ✅ 删除无用列并保存
df_clean = df.drop(columns=["temp", "wind", "wind_day", "wind_night", "weather"], errors='ignore')
df_clean.to_csv("cleaned_weather.csv", index=False, encoding="utf-8")
print("✅ 清洗完成，保存为 cleaned_weather.csv")
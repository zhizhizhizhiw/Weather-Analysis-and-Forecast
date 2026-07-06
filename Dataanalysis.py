import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("cleaned_weather.csv")

# ✅ 转换日期格式
df["date"] = pd.to_datetime(df["date"], format="%Y年%m月%d日", errors="coerce")
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

# ✅ 计算月平均气温（三年平均）
df["temp_avg"] = (df["temp_high"] + df["temp_low"]) / 2
monthly_avg = (
    df[df["year"].between(2022, 2024)]
    .groupby("month")["temp_avg"]
    .mean()
)

# ✅ 绘制月平均气温变化图
plt.figure(figsize=(10, 6))
plt.plot(monthly_avg.index, monthly_avg.values, marker='o', color='tab:red')
for x, y in zip(monthly_avg.index, monthly_avg.values):
    plt.text(x, y, f"{y:.1f}", ha='center', va='bottom')
plt.title("大连市2022–2024年月平均气温变化图（三年平均）")
plt.xlabel("月份")
plt.ylabel("平均气温（℃）")
plt.grid(linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# ✅ 风力等级分布（三年平均）
wind_monthly = (
    df[df["year"].between(2022, 2024)]
    .groupby(["month", "wind_day_level"])
    .size()
    .unstack(fill_value=0)
    .div(3)
)

plt.figure(figsize=(12, 6))
wind_monthly.plot(kind='bar', stacked=True)
plt.title("大连市近三年月风力等级分布图（三年平均）")
plt.xlabel("月份")
plt.ylabel("月均出现天数")
plt.legend(title="风力等级")
plt.tight_layout()
plt.show()

# ✅ 天气状况分布（白天）
weather_day_monthly = (
    df[df["year"].between(2022, 2024)]
    .groupby(["month", "weather_day"])
    .size()
    .unstack(fill_value=0)
    .div(3)
)

plt.figure(figsize=(12, 6))
weather_day_monthly.plot(kind='bar', stacked=True)
plt.title("大连市近三年月日间天气状况分布图（三年平均）")
plt.xlabel("月份")
plt.ylabel("月均出现天数")
plt.legend(title="天气状况")
plt.tight_layout()
plt.show()
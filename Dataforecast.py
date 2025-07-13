import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_percentage_error

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ✅ 读取数据
df = pd.read_csv("cleaned_weather.csv")
df["date"] = pd.to_datetime(df["date"], format="%Y年%m月%d日", errors="coerce")
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

# ✅ 构造月度平均最高温度序列（2022–2024）
monthly_data = (
    df[df["year"].between(2022, 2024)]
    .groupby(["year", "month"])["temp_high"]
    .mean()
    .reset_index()
)
monthly_data["date"] = pd.to_datetime(monthly_data[["year", "month"]].assign(day=1))
monthly_data = monthly_data.sort_values("date")
ts = monthly_data.set_index("date")["temp_high"]

# ✅ 自动选择最佳SARIMA模型（季节性周期=12）
auto_model = auto_arima(
    ts,
    seasonal=True,
    m=12,
    start_p=0, max_p=3,
    start_q=0, max_q=3,
    start_P=0, max_P=2,
    start_Q=0, max_Q=2,
    d=None, D=None,
    trace=True,
    stepwise=True,
    suppress_warnings=True
)
print("✅ 最佳模型参数：", auto_model.order, auto_model.seasonal_order)

# ✅ 拟合SARIMA模型
model = SARIMAX(
    ts,
    order=auto_model.order,
    seasonal_order=auto_model.seasonal_order,
    enforce_stationarity=False,
    enforce_invertibility=False
)
model_fit = model.fit(disp=False)

# ✅ 预测2025年1–6月
forecast = model_fit.forecast(steps=6)
forecast_index = pd.date_range("2025-01-01", periods=6, freq='MS')
forecast_series = pd.Series(forecast, index=forecast_index)

# ✅ 获取2025年真实数据
real_2025 = (
    df[df["year"] == 2025]
    .groupby("month")["temp_high"]
    .mean()
    .reindex(range(1, 7))
)
real_index = pd.to_datetime([f"2025-{m:02d}-01" for m in range(1, 7)])
real_series = pd.Series(real_2025.values, index=real_index)

# ✅ 绘图对比
plt.figure(figsize=(10, 6))
plt.plot(ts.index, ts.values, label="历史月平均最高温度（2022–2024）", marker='o')
plt.plot(forecast_series.index, forecast_series.values, label="预测值（SARIMA）", marker='s')
plt.plot(real_series.index, real_series.values, label="真实值（2025年）", marker='x', linestyle='--')
plt.title("大连市2025年1–6月平均最高温度预测 vs 真实值（SARIMA优化）")
plt.xlabel("月份")
plt.ylabel("平均最高温度（℃）")
plt.legend()
plt.grid(linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# ✅ 计算误差
mape = mean_absolute_percentage_error(real_series, forecast_series)
print(f"✅ MAPE（平均绝对百分比误差）: {mape:.2%}")
# 大连市天气数据分析与预测

基于 Python 的大连市 2022-2025 年天气数据爬取、清洗、可视化分析与温度预测项目。

## 项目概述

从天气后报网站爬取 42 个月的天气历史数据（1332 条），经正则清洗结构化后，进行多维可视化分析，并使用 SARIMA 时间序列模型对 2025 年 1-6 月温度进行预测验证。

## 项目结构

```
├── Dataget.py / DataGet.ipynb           # 爬虫：requests + BeautifulSoup 采集数据
├── Dataanalysis.py / DataAnalyse.ipynb  # 分析：月均气温、风力分布、天气状况可视化
├── Dataforecast.py / DataForecast.ipynb # 预测：auto_arima 选参 + SARIMAX 拟合
├── dalian_weather.csv                   # 原始爬取数据
├── cleaned_weather.csv                  # 清洗后的结构化数据
├── 技术栈全解析.md                        # 各技术栈原理与使用复盘
├── 面试问答精讲.md                        # 常见面试追问及回答思路
└── 实习报告技术要点.md                     # 实习报告核心要点摘要
```

## 技术栈

- **爬虫**：requests + BeautifulSoup4（静态页面解析）
- **数据处理**：pandas（清洗/聚合/透视）+ 正则表达式（字段拆分提取）
- **可视化**：matplotlib（折线图、堆叠柱状图、异常标注）
- **时间序列预测**：pmdarima（auto_arima 自动选参）+ statsmodels（SARIMAX 拟合）
- **评估**：MSE（均方误差），scikit-learn

## 运行步骤

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 如果需要重新爬取数据（可选，仓库已含数据文件）
python Dataget.py

# 3. 数据分析与可视化
python Dataanalysis.py

# 4. 温度预测
python Dataforecast.py
```

Jupyter Notebook 用户可直接运行对应的 `.ipynb` 文件。

## 核心发现

- 大连市气温呈明显年周期波动，冬季 -10℃ ~ 夏季 30℃
- 风力以 3-4 级和 4-5 级为主，冬季风力偏强
- SARIMA(1,0,3) 模型温度预测 MSE ≈ 4.87（均方根误差约 ±2.2℃）
- MAPE 因冬季温度接近 0℃ 产生爆炸——评估指标需匹配数据特性

## 已知限制

- 预测为全量拟合而非严格滚动的 out-of-sample 预测
- 单变量模型（仅温度），未引入湿度、气压等辅助特征
- 数据量有限（3 年训练 / 6 个月验证），更长时间跨度可提升稳定性

---
name: awf-data-science
description: >
  Data analysis workflow — từ raw data đến insights có thể action. EDA, data cleaning,
  visualization, statistical analysis và rút ra insights. Kết hợp tốt với data-scraper-agent
  (thu thập) → awf-data-science (phân tích) → báo cáo.
  Keywords: data analysis, EDA, pandas, visualization, biểu đồ, thống kê, phân tích dữ liệu,
  insight, dataset, CSV, SQL, chart, correlation, distribution, outlier, trend.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-data-science"
skill_version: "1.0.0"
status: active
category: "analysis"
activation: "intent"
priority: "medium"
risk_level: "medium"
allowed_side_effects:
  - "read_data"
  - "generate_report"
requires_confirmation: false
related_workflows:
  - "/review"
  - "/audit"
  - "/brainstorm"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# AWF Data Science — Từ Raw Data Đến Actionable Insights

## Tổng quan
Data không có analysis = noise. Analysis không có question = busywork.
Skill này áp dụng scientific method vào data: bắt đầu từ câu hỏi, dùng data để trả lời, output là insight có thể action.

> 💡 **Triết lý:** "Torture the data long enough and it will confess to anything." — Box. Tránh điều này bằng cách define question TRƯỚC khi nhìn data.

---

## Khi nào kích hoạt

✅ **Triggers:**
- Sau `data-scraper-agent` — đã có data, cần phân tích
- "Phân tích dataset này", "Tìm insights từ data", "Vẽ chart cho..."
- "Correlation giữa X và Y là gì?", "Trend của metric Z ra sao?"
- "Outliers nào trong dataset?", "Segment users theo..."
- Bất kỳ khi nào user có CSV/JSON/SQL data cần hiểu

---

## Quy trình 5 Phase Chuẩn

### Phase 1: QUESTION — Define trước khi nhìn data
```
Business question: [Câu hỏi cụ thể cần trả lời]
Decision được inform: [Quyết định nào sẽ được đưa ra dựa vào kết quả?]
Success metrics: [Kết quả phân tích ra sao thì được coi là thành công?]
Time scope: [Data từ khi nào đến khi nào?]
```

> ⚠️ KHÔNG bắt đầu EDA trước khi có câu hỏi cụ thể. Data exploration không có câu hỏi = academic exercise.

---

### Phase 2: UNDERSTAND — Hiểu dataset

```python
# Quick dataset profiling
import pandas as pd

df = pd.read_csv('data.csv')

print("Shape:", df.shape)
print("\nColumns:", df.dtypes)
print("\nMissing values:\n", df.isnull().sum())
print("\nBasic stats:\n", df.describe())
print("\nDuplicates:", df.duplicated().sum())

# Sample
print("\nFirst 5 rows:\n", df.head())
```

**Checklist sau khi profile:**
- [ ] Bao nhiêu rows, columns?
- [ ] Data types đúng chưa? (int/float/string/datetime)
- [ ] Missing values ở đâu? Bao nhiêu %? → xử lý thế nào?
- [ ] Duplicates có không?
- [ ] Timeframe của data là gì?
- [ ] Key identifier column là gì?

---

### Phase 3: CLEAN — Làm sạch data

**Missing values:**
```python
# Strategy 1: Drop nếu < 5% và random missing
df.dropna(subset=['critical_column'], inplace=True)

# Strategy 2: Fill với median/mode (numerical)
df['price'].fillna(df['price'].median(), inplace=True)

# Strategy 3: Fill với category "Unknown" (categorical)
df['category'].fillna('Unknown', inplace=True)

# Strategy 4: Forward fill (time series)
df['metric'].fillna(method='ffill', inplace=True)
```

**Data type conversion:**
```python
df['date'] = pd.to_datetime(df['date'])
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['category'] = df['category'].astype('category')
```

**Outlier detection:**
```python
# IQR method
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['value'] < Q1 - 1.5*IQR) | (df['value'] > Q3 + 1.5*IQR)]
print(f"Outliers: {len(outliers)} rows ({len(outliers)/len(df)*100:.1f}%)")
```

---

### Phase 4: ANALYZE — Phân tích

#### Univariate — Hiểu từng variable

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Numerical: distribution
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
df['value'].hist(ax=axes[0], bins=30)
axes[0].set_title('Distribution')
df.boxplot(column='value', ax=axes[1])
axes[1].set_title('Boxplot (outliers)')
plt.tight_layout()
plt.savefig('univariate.png')

# Categorical: frequency
df['category'].value_counts().plot(kind='bar', figsize=(10, 4))
plt.title('Category Frequency')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('categories.png')
```

#### Bivariate — Quan hệ giữa 2 variables

```python
# Numerical vs Numerical: scatter + correlation
correlation = df[['metric_a', 'metric_b', 'metric_c']].corr()
sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlation Matrix')
plt.savefig('correlation.png')

# Categorical vs Numerical: group comparison
df.groupby('category')['revenue'].agg(['mean', 'median', 'count']).round(2)
```

#### Time Series — Trend over time

```python
# Resample và plot
df_daily = df.resample('D', on='date')['metric'].sum()
df_daily.plot(figsize=(14, 5))
plt.title('Daily Trend')
plt.xlabel('Date')
plt.ylabel('Metric')

# 7-day moving average để smooth noise
df_daily.rolling(7).mean().plot(label='7-day MA', color='red')
plt.legend()
plt.savefig('trend.png')
```

#### Segmentation — Hiểu sự khác biệt giữa groups

```python
# Compare segments
segment_summary = df.groupby('segment').agg(
    count=('user_id', 'count'),
    avg_revenue=('revenue', 'mean'),
    median_revenue=('revenue', 'median'),
    conversion_rate=('converted', 'mean')
).round(2)
print(segment_summary)
```

---

### Phase 5: SYNTHESIZE — Rút ra insights

**Output format chuẩn:**

```markdown
# Data Analysis Report: [Business Question]
**Dataset:** [Tên & size] | **Period:** [Timeframe] | **Analyzed:** [Date]

## TL;DR — Key Findings
1. **[Insight 1 — actionable]**: [Evidence ngắn gọn]
2. **[Insight 2]**: [Evidence]
3. **[Insight 3]**: [Evidence]

## Detailed Findings

### Finding 1: [Tên rõ ràng]
**Observation:** [Mô tả pattern thấy trong data]
**Evidence:** [Số liệu cụ thể, chart reference]
**Possible explanation:** [Hypothesis — tại sao lại như vậy?]
**Recommended action:** [Làm gì với insight này?]

## Limitations & Caveats
- [Data quality issue nào cần lưu ý?]
- [Correlation ≠ causation — cần test gì thêm?]
- [Missing data ảnh hưởng thế nào?]

## Next Steps
- [ ] [A/B test để validate hypothesis X]
- [ ] [Collect thêm data về Y]
- [ ] [Deep dive vào segment Z]
```

---

## Quick Reference: Chọn Chart gì?

| Tôi muốn thấy... | Dùng chart... |
|-----------------|--------------|
| Distribution của 1 variable | Histogram, Box plot |
| Trend theo thời gian | Line chart |
| So sánh categories | Bar chart |
| Tương quan 2 variables | Scatter plot |
| Phần trăm composition | Pie chart (< 5 categories), Stacked bar |
| Correlation matrix | Heatmap |
| Geographic data | Map (folium, plotly) |
| Funnel/conversion | Funnel chart |

---

## Tích hợp với AWF

| Skill/Workflow | Data Science bổ sung |
|---------------|---------------------|
| `data-scraper-agent` | Scrape → clean → analyze → insight pipeline |
| `awf-research-agent` | Validate research findings bằng quantitative data |
| `awf-diagramming` | Visualize findings dưới dạng diagrams |
| `/brainstorm` | Data-driven brainstorm thay vì assumption-based |
| `psycho-content-engineer` | Audience data → inform content psychology |

---

## ⚠️ Anti-Rationalization

| Sai lầm phổ biến | Thực tế |
|---|---|
| "Correlation này có nghĩa là..." | Correlation ≠ causation. Luôn phải nêu alternatives. |
| "Outliers là lỗi, bỏ đi" | Outliers đôi khi là signals quan trọng nhất. Investigate trước khi drop. |
| "Sample size đủ lớn rồi" | Large N không fix sampling bias. |
| "Visual này cho thấy rõ ràng..." | Axis manipulation can make anything look significant. Be honest. |
| "Data nói lên tất cả" | Data cần context. Số 20% tăng có thể good hoặc bad tùy baseline. |

---

## 🚩 Red Flags

- Bắt đầu plot mà không có câu hỏi cụ thể
- Cherry-pick time range để trend trông đẹp hơn
- Compare absolute numbers khi nên compare rates/percentages
- Không mention data quality issues trong report
- "Action" recommendations quá chung chung: "cần cải thiện metric X"
- Không phân biệt correlation vs causation trong conclusions

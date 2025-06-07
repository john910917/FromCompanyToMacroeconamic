import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
import numpy as np

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取數據
usd_ntd_df = pd.read_csv('歷史美對台.csv')
corn_df = pd.read_csv('玉米期貨歷史數據.csv')

# 轉換日期格式
usd_ntd_df['日期'] = pd.to_datetime(usd_ntd_df['日期'])
corn_df['日期'] = pd.to_datetime(corn_df['日期'])

# 合併數據
merged_df = pd.merge(usd_ntd_df, corn_df, on='日期', how='inner')

# 計算進口商成本
merged_df['進口商成本'] = merged_df['收市_x'] * merged_df['收市_y']

# 計算匯率變動對成本的影響
merged_df['匯率變動'] = merged_df['收市_x'].pct_change()
merged_df['成本變動'] = merged_df['進口商成本'].pct_change()

# 計算匯率每變動1%對成本的影響
impact_analysis = merged_df[['匯率變動', '成本變動']].dropna()
impact_ratio = impact_analysis['成本變動'] / impact_analysis['匯率變動']
avg_impact = impact_ratio.mean()

print(f"\n匯率變動對進口商成本的影響分析：")
print(f"平均而言，匯率每升值1%，進口商成本下降約 {abs(avg_impact):.2f}%")

# 繪製圖表
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12), height_ratios=[1, 1, 1])
fig.patch.set_facecolor('#f0f0f0')

# 繪製匯率走勢
ax1.plot(merged_df['日期'], merged_df['收市_x'], color='#1E88E5', linewidth=2.5, label='美對台匯率')
ax1.set_ylabel('匯率 (NTD/USD)', color='#1E88E5', fontsize=12, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#1E88E5')
ax1.grid(True, alpha=0.3)
ax1.set_title('美對台匯率走勢', fontsize=14, fontweight='bold', pad=20)

# 繪製玉米期貨價格
ax2.plot(merged_df['日期'], merged_df['收市_y'], color='#43A047', linewidth=2.5, label='玉米期貨價格')
ax2.set_ylabel('價格 (USD)', color='#43A047', fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#43A047')
ax2.grid(True, alpha=0.3)
ax2.set_title('玉米期貨價格走勢', fontsize=14, fontweight='bold', pad=20)

# 繪製進口商成本
ax3.bar(merged_df['日期'], merged_df['進口商成本'], color='#E53935', width=8, label='進口商成本')
ax3.set_ylabel('成本 (NTD)', color='#E53935', fontsize=12, fontweight='bold')
ax3.tick_params(axis='y', labelcolor='#E53935')
ax3.grid(True, alpha=0.3)
ax3.set_title('進口商成本', fontsize=14, fontweight='bold', pad=20)

# 設定x軸格式
for ax in [ax1, ax2, ax3]:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

# 調整布局
plt.tight_layout()

# 儲存圖表
plt.savefig('美對台匯率、玉米期貨價格與進口商成本對照圖.png', dpi=300, bbox_inches='tight')
plt.close()

# 繪製匯率變動與成本變動的散點圖
plt.figure(figsize=(10, 6))
plt.scatter(impact_analysis['匯率變動'] * 100, impact_analysis['成本變動'] * 100, 
           alpha=0.5, color='#1E88E5')
plt.xlabel('匯率變動 (%)', fontsize=12, fontweight='bold')
plt.ylabel('成本變動 (%)', fontsize=12, fontweight='bold')
plt.title('匯率變動與進口商成本變動關係', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# 添加趨勢線
z = np.polyfit(impact_analysis['匯率變動'] * 100, impact_analysis['成本變動'] * 100, 1)
p = np.poly1d(z)
plt.plot(impact_analysis['匯率變動'] * 100, p(impact_analysis['匯率變動'] * 100), 
         "r--", alpha=0.8, label=f'趨勢線 (斜率: {z[0]:.2f})')
plt.legend()

plt.tight_layout()
plt.savefig('匯率變動與成本變動關係圖.png', dpi=300, bbox_inches='tight')
plt.close() 
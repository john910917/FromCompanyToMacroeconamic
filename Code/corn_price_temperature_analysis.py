import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import seaborn as sns

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取玉米期貨數據
corn_df = pd.read_csv('長天期玉米期貨.CSV')
corn_df['日期'] = pd.to_datetime(corn_df['日期'])

# 讀取氣溫數據
temp_df = pd.read_csv('愛荷華州平均氣溫.CSV')
temp_df = temp_df.iloc[:-1]  # 移除最後一行（平均值）

# 將氣溫數據轉換為長格式
temp_df = temp_df.melt(id_vars=['Unnamed: 0'], 
                      value_vars=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 
                                'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
                      var_name='月份', value_name='氣溫')

# 創建日期列
temp_df['年份'] = temp_df['Unnamed: 0'].astype(str)
temp_df['日期'] = pd.to_datetime(temp_df['年份'] + '-' + temp_df['月份'] + '-1', format='%Y-%b-%d', errors='coerce')

temp_df = temp_df.dropna(subset=['日期'])  # 移除無法轉換的日期

# 合併玉米期貨價格與氣溫數據
df = pd.merge(corn_df, temp_df, on='日期', how='inner')

# 計算相關係數
corr = df['氣溫'].corr(df['收市'])
print(f"氣溫與玉米價格的相關係數：{corr:.2f}")

# 新增氣溫滯後一期
df['temp_lag1'] = df['氣溫'].shift(1)

# 繪製散佈圖（原始氣溫）
plt.figure(figsize=(10, 6))
sns.regplot(x='氣溫', y='收市', data=df)
plt.xlabel('愛荷華州每月平均氣溫 (°F)')
plt.ylabel('玉米期貨價格（美元）')
plt.title('氣溫 vs 玉米期貨價格 散佈圖')
plt.grid(True)
plt.tight_layout()
plt.savefig('氣溫vs玉米期貨價格散佈圖.png', dpi=300, bbox_inches='tight')
plt.show()

# 繪製滯後氣溫散佈圖
plt.figure(figsize=(10, 6))
sns.regplot(x='temp_lag1', y='收市', data=df)
plt.xlabel('愛荷華州每月平均氣溫（滯後一期）(°F)')
plt.ylabel('玉米期貨價格（美元）')
plt.title('滯後氣溫 vs 玉米期貨價格 散佈圖')
plt.grid(True)
plt.tight_layout()
plt.savefig('滯後氣溫vs玉米期貨價格散佈圖.png', dpi=300, bbox_inches='tight')
plt.show()

# 繪製時間序列對照圖
fig, ax1 = plt.subplots(figsize=(15, 8))

# 繪製玉米期貨價格（左Y軸）
line1 = ax1.plot(corn_df['日期'], corn_df['收市'], 
                label='玉米期貨價格', 
                color='#1E88E5',  # 深藍色
                linewidth=2.5)
ax1.set_ylabel('玉米期貨價格 (美元)', fontsize=12, color='#1E88E5')
ax1.tick_params(axis='y', labelcolor='#1E88E5')

# 創建第二個Y軸
ax2 = ax1.twinx()

# 繪製氣溫資料為柱狀圖（右Y軸）
bar2 = ax2.bar(temp_df['日期'], temp_df['氣溫'], 
               width=20, label='愛荷華州平均氣溫', 
               color='#E53935', alpha=0.5, edgecolor='white')
ax2.set_ylabel('平均氣溫 (°F)', fontsize=12, color='#E53935')
ax2.tick_params(axis='y', labelcolor='#E53935')

# 設置標題和網格
plt.title('玉米期貨價格與愛荷華州氣溫對照圖', fontsize=14, pad=20)
ax1.grid(True, linestyle='--', alpha=0.5)

# 設置x軸日期格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gcf().autofmt_xdate()

# 合併圖例
lines = line1 + [bar2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

# 調整布局
plt.tight_layout()

# 保存圖表
plt.savefig('玉米期貨價格與氣溫對照圖.png', dpi=300, bbox_inches='tight')
plt.show() 
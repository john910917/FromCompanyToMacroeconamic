import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取玉米期貨數據
corn_df = pd.read_csv('玉米期貨歷史數據.csv')
corn_df['日期'] = pd.to_datetime(corn_df['日期'])

# 讀取公司營收數據
df1 = pd.read_csv('大成.csv', encoding='big5')
df2 = pd.read_csv('卜蜂.csv', encoding='big5')

# 處理營收數據
df1['公司'] = '大成'
df2['公司'] = '卜蜂'
df_all = pd.concat([df1, df2], ignore_index=True)
df_all['年月'] = pd.to_datetime(df_all['年月'], format='%Y%m')
df_all['營收'] = pd.to_numeric(df_all['單月營收(千元)'])

# 創建圖表和雙Y軸
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

# 繪製玉米期貨價格（左Y軸）
line1 = ax1.plot(corn_df['日期'], corn_df['收市'], 
                label='玉米期貨價格', 
                color='#1E88E5',  # 深藍色
                linewidth=2.5)
ax1.set_ylabel('玉米期貨價格 (美元)', fontsize=10, color='#1E88E5')
ax1.tick_params(axis='y', labelcolor='#1E88E5')

# 繪製公司營收（右Y軸）- 使用柱狀圖
bar_width = 8  # 調整柱狀圖寬度
for i, (company, group) in enumerate(df_all.groupby('公司')):
    if company == '大成':
        color = '#43A047'  # 深綠色
        offset = -bar_width/2
    else:
        color = '#E53935'  # 深紅色
        offset = bar_width/2
    
    # 繪製柱狀圖
    bars = ax2.bar(group['年月'] + pd.Timedelta(days=offset), 
                  group['營收'], 
                  width=bar_width,
                  label=f'{company}營收',
                  color=color,
                  alpha=0.85)

ax2.set_ylabel('營收 (千元)', fontsize=10)

# 合併圖例
lines = line1
labels = [l.get_label() for l in lines]
handles = lines + ax2.get_legend_handles_labels()[0]
labels.extend(ax2.get_legend_handles_labels()[1])
ax1.legend(handles, labels, loc='upper left')

# 設置標題和網格
plt.title('玉米期貨價格與公司營收對照圖', fontsize=14, pad=20)
ax1.grid(True, linestyle='--', alpha=0.5)

# 設置x軸日期格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.gcf().autofmt_xdate()

# 調整布局
plt.tight_layout()

# 保存圖表
plt.savefig('玉米期貨價格與營收對照圖.png', dpi=300, bbox_inches='tight')
plt.show() 
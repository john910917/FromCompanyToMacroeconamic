import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取玉米期貨數據
corn_df = pd.read_csv('長天期玉米期貨.CSV')
corn_df['日期'] = pd.to_datetime(corn_df['日期'])

# 創建圖表
fig, ax1 = plt.subplots(figsize=(15, 8))

# 繪製玉米期貨價格
line1 = ax1.plot(corn_df['日期'], corn_df['收市'], 
                label='玉米期貨價格', 
                color='#1E88E5',  # 深藍色
                linewidth=2.5)

# 設置Y軸標籤
ax1.set_ylabel('玉米期貨價格 (美元)', fontsize=12, color='#1E88E5')
ax1.tick_params(axis='y', labelcolor='#1E88E5')

# 設置標題和網格
plt.title('玉米期貨價格走勢圖 (2010-2025)', fontsize=14, pad=20)
ax1.grid(True, linestyle='--', alpha=0.5)

# 設置x軸日期格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gcf().autofmt_xdate()

# 添加圖例
ax1.legend(loc='upper left')

# 調整布局
plt.tight_layout()

# 保存圖表
plt.savefig('玉米期貨價格走勢圖.png', dpi=300, bbox_inches='tight')
plt.show()
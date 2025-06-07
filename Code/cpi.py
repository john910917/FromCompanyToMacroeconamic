import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import re

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取CPI數據
df = pd.read_csv('cpi.csv', encoding='big5', skiprows=3)

# 重新命名欄位
df.columns = ['年月', '總指數', '核心CPI', 'Unnamed: 3']

# 民國年轉西元年
def roc_to_ad(roc_str):
    match = re.match(r'(\d+)年(\d+)月', str(roc_str))
    if match:
        year = int(match.group(1)) + 1911
        month = int(match.group(2))
        return f'{year}-{month:02d}'
    return None

df['年月'] = df['年月'].apply(roc_to_ad)
df = df.dropna(subset=['年月'])
df['年月'] = pd.to_datetime(df['年月'], format='%Y-%m')

# 將數值欄位轉換為浮點數
df['總指數'] = pd.to_numeric(df['總指數'], errors='coerce')
df['核心CPI'] = pd.to_numeric(df['核心CPI'], errors='coerce')

# 依照時間排序
df = df.sort_values('年月')

# 計算年增率
df['總指數年增率'] = df['總指數'].pct_change(12) * 100
df['核心CPI年增率'] = df['核心CPI'].pct_change(12) * 100

# 創建圖表
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# 繪製CPI指數走勢圖
ax1.plot(df['年月'], df['總指數'], label='總指數', linewidth=2)
ax1.plot(df['年月'], df['核心CPI'], label='食物類', linewidth=2)
ax1.set_title('CPI指數走勢圖', fontsize=14)
ax1.set_xlabel('日期', fontsize=12)
ax1.set_ylabel('指數', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

# 繪製年增率走勢圖
ax2.plot(df['年月'], df['總指數年增率'], label='總指數年增率', linewidth=2)
ax2.plot(df['年月'], df['核心CPI年增率'], label='食物類年增率', linewidth=2)
ax2.set_title('CPI年增率走勢圖', fontsize=14)
ax2.set_xlabel('日期', fontsize=12)
ax2.set_ylabel('年增率(%)', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend()

# 設定x軸日期格式
for ax in [ax1, ax2]:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

# 調整布局
plt.tight_layout()

# 儲存圖表
plt.savefig('CPI分析圖.png', dpi=300, bbox_inches='tight')
plt.show()

# 計算年平均通膨率
latest_year = df['年月'].dt.year.max()
yearly_avg = df[df['年月'].dt.year == latest_year]['總指數年增率'].mean()

print(f'\n{latest_year}年平均通膨率：{yearly_avg:.2f}%')

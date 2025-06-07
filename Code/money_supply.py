import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取貨幣總數數據
df_money = pd.read_csv('貨幣總數.csv', encoding='utf-8')
df_money.columns = ['年月', 'M1B原始值', 'M2原始值']

# 處理貨幣供給數據
# 轉換日期格式
df_money['年月'] = pd.to_datetime(df_money['年月'].str.replace('M', '-'), format='%Y-%m')

# 數值轉換（處理千分位符號）
df_money['M1B原始值'] = df_money['M1B原始值'].str.replace(',', '').astype(float)
df_money['M2原始值'] = df_money['M2原始值'].str.replace(',', '').astype(float)

# 依照時間排序
df_money = df_money.sort_values('年月')

# 計算年增率
df_money['M1B年增率'] = df_money['M1B原始值'].pct_change(periods=12) * 100
df_money['M2年增率'] = df_money['M2原始值'].pct_change(periods=12) * 100
df_money['M1B-M2'] = df_money['M1B年增率'] - df_money['M2年增率']

# 創建圖表
fig, ax1 = plt.subplots(figsize=(12, 6))

# 繪製年增率走勢圖（折線圖）
line1 = ax1.plot(df_money['年月'], df_money['M1B年增率'], label='M1B年增率', linewidth=2)
line2 = ax1.plot(df_money['年月'], df_money['M2年增率'], label='M2年增率', linewidth=2)

# 設定第一個Y軸
ax1.set_ylabel('年增率(%)', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.7)

# 創建第二個Y軸
ax2 = ax1.twinx()

# 繪製M1B-M2柱狀圖
bars = ax2.bar(df_money['年月'], df_money['M1B-M2'], width=20, alpha=0.3, label='M1B-M2')
# 設定柱狀圖顏色
for bar in bars:
    if bar.get_height() >= 0:
        bar.set_color('red')
    else:
        bar.set_color('green')

# 設定第二個Y軸
ax2.set_ylabel('M1B-M2差額(%)', fontsize=12)

# 設定圖表標題
plt.title('M1B與M2年增率走勢及差額', fontsize=14)

# 設定x軸日期格式
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gcf().autofmt_xdate()  # 自動旋轉日期標籤

# 合併圖例
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines + [bars], labels + ['M1B-M2'], fontsize=10)

# 調整布局
plt.tight_layout()

# 儲存圖表
plt.savefig('貨幣供給年增率走勢圖.png', dpi=300, bbox_inches='tight')
plt.show()

# 顯示最新數據
latest_m1b = df_money['M1B原始值'].iloc[-1]
latest_m2 = df_money['M2原始值'].iloc[-1]
latest_m1b_yoy = df_money['M1B年增率'].iloc[-1]
latest_m2_yoy = df_money['M2年增率'].iloc[-1]
latest_diff = df_money['M1B-M2'].iloc[-1]
print(f'\n最新M1B：{latest_m1b:,.0f}億元')
print(f'最新M2：{latest_m2:,.0f}億元')
print(f'最新M1B年增率：{latest_m1b_yoy:.2f}%')
print(f'最新M2年增率：{latest_m2_yoy:.2f}%')
print(f'最新M1B-M2差額：{latest_diff:.2f}%') 
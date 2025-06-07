import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取市值資料
df_dacheng = pd.read_csv('大成市值.csv', encoding='big5')
df_bofeng = pd.read_csv('卜蜂市值.csv', encoding='big5')

# 將日期欄位轉換為datetime格式
df_dacheng['年月'] = pd.to_datetime(df_dacheng['年月'], format='%Y%m')
df_bofeng['年月'] = pd.to_datetime(df_bofeng['年月'], format='%Y%m')

# 創建圖表
plt.figure(figsize=(12, 6))

# 繪製市值走勢圖
plt.plot(df_dacheng['年月'], df_dacheng['市值(百萬元)'], label='大成', linewidth=2)
plt.plot(df_bofeng['年月'], df_bofeng['市值(百萬元)'], label='卜蜂', linewidth=2)

# 設定圖表標題和標籤
plt.title('大成與卜蜂市值比較圖', fontsize=14)
plt.xlabel('日期', fontsize=12)
plt.ylabel('市值（百萬元）', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# 設定x軸日期格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gcf().autofmt_xdate()  # 自動旋轉日期標籤

# 加入圖例
plt.legend(fontsize=10)

# 調整布局
plt.tight_layout()

# 儲存圖表
plt.savefig('大成卜蜂市值比較圖.png', dpi=300, bbox_inches='tight')
plt.show()

# 計算並顯示最新市值
latest_dacheng = df_dacheng['市值(百萬元)'].iloc[-1]
latest_bofeng = df_bofeng['市值(百萬元)'].iloc[-1]
print(f'\n最新市值比較（百萬元）：')
print(f'大成：{latest_dacheng:,.0f}')
print(f'卜蜂：{latest_bofeng:,.0f}')
print(f'市值差距：{abs(latest_dacheng - latest_bofeng):,.0f}')

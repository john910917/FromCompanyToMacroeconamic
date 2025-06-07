import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取台銀利率數據
df_rate = pd.read_csv('台銀利率.csv', encoding='big5')
df_rate.columns = ['年月', '利率']

# 處理台銀利率數據
# 轉換日期格式
df_rate['年月'] = pd.to_datetime(df_rate['年月'].astype(str).str.zfill(6), format='%Y%m')

# 數值轉換
df_rate['利率'] = pd.to_numeric(df_rate['利率'], errors='coerce')

# 依照時間排序
df_rate = df_rate.sort_values('年月')

# 創建圖表
plt.figure(figsize=(12, 6))

# 繪製台銀利率走勢圖
plt.plot(df_rate['年月'], df_rate['利率'], label='台銀利率', linewidth=2, color='red')

# 設定圖表標題和標籤
plt.title('台銀基準利率走勢圖', fontsize=14)
plt.xlabel('日期', fontsize=12)
plt.ylabel('利率(%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# 設定x軸日期格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gcf().autofmt_xdate()  # 自動旋轉日期標籤

# 加入圖例
plt.legend(fontsize=10)

# 調整布局
plt.tight_layout()

# 儲存圖表
plt.savefig('台銀基準利率走勢圖.png', dpi=300, bbox_inches='tight')
plt.show()

# 顯示最新利率
latest_rate = df_rate['利率'].iloc[-1]
print(f'\n最新台銀利率：{latest_rate:.3f}%') 
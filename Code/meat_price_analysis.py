import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取豬隻雞肉價格資料
# 嘗試使用 big5 編碼讀取

df = pd.read_csv('豬隻雞肉價格.csv', encoding='big5')

# 將 '年月' 轉換為日期時間格式
df['年月'] = pd.to_datetime(df['年月'], format='%Y%m')

# 將價格欄位轉換為數值型態 (可能需要處理非數字字元)
# 假設價格欄位是除了 '年月' 以外的所有欄位
price_cols = df.columns.tolist()
price_cols.remove('年月')

# 繪製趨勢圖
plt.figure(figsize=(12, 7))

for col in price_cols:
    plt.plot(df['年月'], df[col], linestyle='-', label=col)

# 設定圖表標題和標籤
plt.title('豬隻與雞肉價格趨勢', fontsize=16)
plt.xlabel('年份', fontsize=12)
plt.ylabel('價格 (元)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# 設定 x 軸日期格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator()) # 以年份為主要刻度
plt.xticks(rotation=45)

# 調整布局以避免標籤重疊
plt.tight_layout()

# 儲存圖表
plt.savefig('豬隻雞肉價格趨勢圖.png', dpi=300)

# 顯示圖表
plt.show()

# 顯示最新價格數據
latest_data = df.iloc[-1]
print('\n最新價格數據：')
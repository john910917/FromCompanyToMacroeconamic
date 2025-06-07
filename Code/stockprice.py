import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取兩個CSV檔案
df_dacheng = pd.read_csv('大成股價.csv', encoding='big5')
df_bofeng = pd.read_csv('卜蜂股價.csv', encoding='big5')

# 將日期欄位轉換為datetime格式
df_dacheng['年月'] = pd.to_datetime(df_dacheng['年月'], format='%Y%m')
df_bofeng['年月'] = pd.to_datetime(df_bofeng['年月'], format='%Y%m')

# 創建三個子圖
fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(14, 15))

# 1. 股價走勢圖（收盤價折線圖）
ax0.plot(df_dacheng['年月'], df_dacheng['收盤價(元)'], label='大成', linewidth=2)
ax0.plot(df_bofeng['年月'], df_bofeng['收盤價(元)'], label='卜蜂', linewidth=2)
ax0.set_title('大成與卜蜂股價走勢圖', fontsize=14)
ax0.set_xlabel('日期', fontsize=12)
ax0.set_ylabel('收盤價', fontsize=12)
ax0.grid(True, linestyle='--', alpha=0.7)
ax0.legend(fontsize=10)
ax0.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# 2. 本益比直方圖
ax1.bar(df_dacheng['年月'], df_dacheng['本益比-TSE'], width=15, alpha=0.5, label='大成')
ax1.bar(df_bofeng['年月'], df_bofeng['本益比-TSE'], width=15, alpha=0.5, label='卜蜂')
ax1.set_title('本益比比較', fontsize=14)
ax1.set_xlabel('日期', fontsize=12)
ax1.set_ylabel('本益比', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# 3. 現金股利率直方圖
ax2.bar(df_dacheng['年月'], df_dacheng['現金股利率'], width=15, alpha=0.5, label='大成')
ax2.bar(df_bofeng['年月'], df_bofeng['現金股利率'], width=15, alpha=0.5, label='卜蜂')
ax2.set_title('現金股利率比較', fontsize=14)
ax2.set_xlabel('日期', fontsize=12)
ax2.set_ylabel('現金股利率', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend()
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# 日期標籤旋轉
for ax in [ax0, ax1, ax2]:
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

# 調整布局
plt.tight_layout()

# 儲存圖表
plt.savefig('大成卜蜂_股價本益比現金殖利率.png', dpi=300, bbox_inches='tight')
plt.show()

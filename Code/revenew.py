import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 設定中文字型和負號顯示
plt.rcParams['font.family'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False

# 載入兩間公司資料
df1 = pd.read_csv('大成.csv', encoding='big5')   # or .csv
df2 = pd.read_csv('卜蜂.csv', encoding='big5')

# 加入公司名稱欄位
df1['公司'] = '大成'
df2['公司'] = '卜蜂'

# 合併兩份資料
df_all = pd.concat([df1, df2], ignore_index=True)

# 轉換時間格式與數值欄位
df_all['年月'] = pd.to_datetime(df_all['年月'], format='%Y%m')
df_all['營收'] = pd.to_numeric(df_all['單月營收(千元)'])
df_all['單月營收與上月比％'] = pd.to_numeric(df_all['單月營收與上月比％'])

# 畫圖：營收比較
plt.figure(figsize=(12, 6))

# 取得所有年月排序後作為x軸
all_dates = sorted(df_all['年月'].unique())

# 設定bar的寬度和位置
bar_width = 1 / len(df_all['公司'].unique())  # 每家公司一組的bar寬度
x = np.arange(len(all_dates))  # x軸的位置

print(df_all['年月'])

# 依公司分組畫bar，稍微往右偏移以避免重疊
for i, (company, group) in enumerate(df_all.groupby('公司')):
    # 對齊x軸
    # group['年月']是時間，要轉換成x軸的index
    values = []
    for date in all_dates:
        val = group[group['年月'] == date]['單月營收與上月比％']
        values.append(val.values[0] if not val.empty else 0)  # 沒資料用0填補

    plt.bar(x + i * bar_width, values, width=bar_width, label=company)

plt.title('單月營收比較')
plt.xlabel('年月')
plt.ylabel('單月營收與上月比％')
plt.xticks(
    x + bar_width * (len(df_all['公司'].unique()) - 1) / 2,
    [d.strftime('%y/%m') for d in all_dates],
    rotation=75
)
plt.legend()
plt.grid(True, axis='y')  # 只在y軸顯示格線
plt.tight_layout()
plt.show()
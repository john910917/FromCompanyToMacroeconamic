import pandas as pd
import matplotlib.pyplot as plt

# 兩間公司檔案與編碼
files = ['大成.csv', '卜蜂.csv']
company_names = ['大成', '卜蜂']
encodings = ['big5', 'big5']

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 儲存所有公司資料
all_data = []

for i, file in enumerate(files):
    print(f'\n===== {company_names[i]} 統計資料 =====')
    df = pd.read_csv(file, encoding=encodings[i])
    # 數值轉換
    if '單月營收(千元)' in df.columns:
        df['單月營收(千元)'] = pd.to_numeric(df['單月營收(千元)'].astype(str).str.replace(',', ''), errors='coerce')
    if '年月' in df.columns:
        df['年月'] = df['年月'].astype(str)
        df = df.sort_values('年月')
    df['公司'] = company_names[i]
    all_data.append(df)

# 合併所有公司資料
all_df = pd.concat(all_data, ignore_index=True)

# 各公司單月營收長條圖（X軸：年月，Y軸：單月營收）
for company in company_names:
    sub = all_df[all_df['公司'] == company]
    plt.figure(figsize=(12, 6))
    plt.bar(sub['年月'], sub['單月營收(千元)'])
    plt.title(f'{company} - 單月營收(千元) 時間序列長條圖')
    plt.xlabel('年月')
    plt.ylabel('單月營收(千元)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 計算並繪製成長率折線圖
plt.figure(figsize=(12, 6))
for company in company_names:
    sub = all_df[all_df['公司'] == company].copy()
    # 計算月成長率，明確指定 fill_method=None
    sub['成長率'] = sub['單月營收(千元)'].pct_change(fill_method=None) * 100
    plt.plot(sub['年月'], sub['成長率'], marker='o', label=company)

plt.title('兩公司營收成長率比較')
plt.xlabel('年月')
plt.ylabel('成長率 (%)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# 繪製成長率直方圖
plt.figure(figsize=(12, 6))
for company in company_names:
    sub = all_df[all_df['公司'] == company].copy()
    sub['成長率'] = sub['單月營收(千元)'].pct_change(fill_method=None) * 100
    plt.hist(sub['成長率'].dropna(), bins=20, alpha=0.5, label=company)

plt.title('兩公司營收成長率分布')
plt.xlabel('成長率 (%)')
plt.ylabel('頻率')
plt.legend()
plt.tight_layout()
plt.show()

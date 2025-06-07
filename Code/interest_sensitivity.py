import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取利率敏感度數據
df_sensitivity = pd.read_csv('利率敏感度(營收).csv', encoding='big5')
df_sensitivity.columns = ['年月', '公司1', '營收1', '公司2', '營收2', '利率']

# 處理數據
# 轉換日期格式
df_sensitivity['年月'] = pd.to_datetime(df_sensitivity['年月'].astype(str).str.zfill(6), format='%Y%m')

# 數值轉換
df_sensitivity['營收1'] = df_sensitivity['營收1'].astype(float)
df_sensitivity['營收2'] = df_sensitivity['營收2'].astype(float)
df_sensitivity['利率'] = df_sensitivity['利率'].astype(float)

# 依照時間排序
df_sensitivity = df_sensitivity.sort_values('年月')

# 計算利率敏感度
X = df_sensitivity[['利率']]

# 卜蜂敏感度
model_bufeng = LinearRegression().fit(X, df_sensitivity['營收1'])
sensitivity_bufeng = model_bufeng.coef_[0]

# 大成敏感度
model_dacheng = LinearRegression().fit(X, df_sensitivity['營收2'])
sensitivity_dacheng = model_dacheng.coef_[0]

# 總營收敏感度
df_sensitivity['總營收'] = df_sensitivity['營收1'] + df_sensitivity['營收2']
model_total = LinearRegression().fit(X, df_sensitivity['總營收'])
sensitivity_total = model_total.coef_[0]

# 創建圖表
plt.figure(figsize=(10, 6))

# 設定柱狀圖數據
companies = ['卜蜂', '大成', '總營收']
colors = ['#FF9999', '#66B2FF', '#99FF99']

# 計算敏感度（以金額表示）
sensitivities = [
    sensitivity_bufeng,
    sensitivity_dacheng,
    sensitivity_total
]

# 繪製柱狀圖
bars = plt.bar(companies, sensitivities, color=colors)
plt.title('利率敏感度分析 (基準：1%)', fontsize=14)
plt.ylabel('營收變化金額(千元)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# 在柱狀圖上方顯示數值
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.0f}',
             ha='center', va='bottom')

# 調整布局
plt.tight_layout()

# 儲存圖表
plt.savefig('利率敏感度分析圖.png', dpi=300, bbox_inches='tight')
plt.show()

# 顯示利率敏感度
print('\n利率敏感度分析 (基準：1%)：')
print(f'卜蜂利率敏感度：{sensitivities[0]:,.0f}千元/1%')
print(f'大成利率敏感度：{sensitivities[1]:,.0f}千元/1%')
print(f'總營收利率敏感度：{sensitivities[2]:,.0f}千元/1%')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 建立資料
data = pd.read_csv('員工資料.csv', encoding='big5')

df = pd.DataFrame(data)

# 計算平均薪資
df["平均薪資(仟元/人)"] = df["員工薪資(仟元)"] / df["員工人數(人)"]

# 分公司繪圖並儲存成獨立圖片
companies = df["公司名稱"].unique()

figures = [] # 用於儲存圖形對象

for company in companies:
    company_data = df[df["公司名稱"] == company]
    years = company_data["年月"]

    # 圖1: 薪資總額和平均薪資趨勢圖 (雙軸圖)
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    figures.append(fig1) # 將圖形對象加入列表

    ax1.plot(years, company_data["員工薪資(仟元)"], marker='o', label="薪資總額")
    ax1.set_title(f"{company} - 薪資總額與平均薪資趨勢")
    ax1.set_xlabel("年度")
    ax1.set_ylabel("薪資總額(仟元)")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(years, company_data["平均薪資(仟元/人)"], marker='^', color='green', label="平均薪資")
    ax2.set_ylabel("仟元/人", color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # 合併圖例
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.tight_layout()
    plt.savefig(f'{company}_薪資與平均薪資趨勢圖.png')
    # plt.close(fig1) # 移除關閉圖形的指令

    # 圖2: 每股盈餘趨勢圖 (柱狀圖)
    fig2, ax3 = plt.subplots(figsize=(10, 6))
    figures.append(fig2) # 將圖形對象加入列表

    bars = ax3.bar(years, company_data["每股盈餘(元/股)"], color="orange", label="EPS")
    ax3.set_title(f"{company} - 每股盈餘趨勢")
    ax3.set_xlabel("年度")
    ax3.set_ylabel("元/股")
    ax3.grid(False) # 不顯示網格線
    ax3.legend()

    # 在柱狀圖上方顯示數值
    for bar in bars:
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., yval,
                f'{yval:.2f}',
                ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(f'{company}_每股盈餘趨勢圖.png')
    # plt.close(fig2) # 移除關閉圖形的指令

# 在所有圖形都建立和儲存後，使用 plt.show() 顯示所有圖形
plt.show()

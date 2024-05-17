import pandas as pd
import os

# 指定csv文件夹路径
data_folder_path = '/Users/wangnan/Desktop/UBS/data'

# csv文件名
csv_file_name = 'trade-price-ir-vegas.csv'

# 完整的csv文件路径
csv_file_path = f'{data_folder_path}/{csv_file_name}'

# 使用panadas的read_csv()函数读取cvs文件，并将其存储为dataframe
data = pd.read_csv(csv_file_path)
print(data.head(5))


# 获取所有不同的类别
dummyTrade_name = ['dummyTrade1', 'dummyTrade2', 'dummyTrade3', 'dummyTrade4', 'dummyTrade5', 'dummyTrade6',
                   'dummyTrade7', 'dummyTrade8', 'dummyTrade9', 'dummyTrade10', 'dummyTrade11', 'dummyTrade12']

# 遍历每个类别
for dTrade in dummyTrade_name:
    # 根据类别筛选数据
    dTrade_data = data[data['Trade Name'] == dTrade]
    # 生成文件名
    filename = f"{dTrade}_data.csv"
    print(filename)
    # 将数据保存到新的csv文件中，文件名格式为dTrade_data.csv
    dTrade_data.to_csv(filename, index=False)
    print(f"Saved {filename}")


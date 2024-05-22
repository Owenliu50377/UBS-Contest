import pandas as pd

# 指定csv文件夹路径
data_folder_path = '/Users/wangnan/Desktop/UBS/data'

# csv文件名
dummyTrade_file_name = 'trade-information.csv'
vegas_file_name = 'trade-price-ir-vegas.csv'

# 完整的csv文件路径
dummyTrade_file_path = f'{data_folder_path}/{dummyTrade_file_name}'
vegas_file_path = f'{data_folder_path}/{vegas_file_name}'

# 使用panadas的read_csv()函数读取cvs文件，并将其存储为dataframe
dummyTrade_info = pd.read_csv(dummyTrade_file_path)
print(dummyTrade_info.head(5))
vegas_data = pd.read_csv(vegas_file_path)
print(vegas_data.head(5))


# 将pay_frequency字符串映射为相应的数值
pay_frequency_mapping = {
    '6M': 0.5,
    '4M': 0.333,
    '3M': 0.25
}
dummyTrade_info['pay_frequency'] = dummyTrade_info['pay_frequency'].map(pay_frequency_mapping)

# 将maturity字符串映射为相应的数值
maturity_mapping = {
    '5Y': 5,
    '10Y': 10
}
dummyTrade_info['maturity'] = dummyTrade_info['maturity'].map(maturity_mapping)

print("Transformed dummyTrade_info results:")
print(dummyTrade_info.head(8))


# 使用 merge() 函数合并两个表格，根据 Trade Name 进行连接
merged_data = pd.merge(vegas_data, dummyTrade_info, how='left', left_on='Trade Name', right_on='trade name')

# 删除 'trade name' 列
merged_data.drop(columns=['trade name'], inplace=True)

print("Merged datasets results:")
print(merged_data.head(3))

# 将数据保存到新的csv文件中，文件名格式为merged_data.csv
filename = f"merged_data.csv"
merged_data.to_csv(filename, index=False)
print(f"Saved {filename}")

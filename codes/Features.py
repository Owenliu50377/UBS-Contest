import pandas as pd

# 读取数据文件
CMS_data = pd.read_csv("/Users/wangnan/Desktop/UBS/data/market-data-swap-rates.csv")
trade_info = pd.read_csv("/Users/wangnan/Desktop/UBS/data/trade-information.csv")

# Pay Frequency 特征架构
# 将pay_frequency字符串映射为相应的数值
pay_frequency_mapping = {
    '6M': 2,
    '4M': 3,
    '3M': 4
}
trade_info['pay_frequency'] = trade_info['pay_frequency'].map(pay_frequency_mapping)

# Maturity 特征架构
# 将maturity字符串映射为相应的数值
maturity_mapping = {
    '5Y': 5,
    '10Y': 10
}
trade_info['maturity'] = trade_info['maturity'].map(maturity_mapping)

# Underlying Assets 特征架构
# Lower Bound & Upper Bound 特征架构

# 创建underlying到Tenor的映射关系
underlying_to_tenor = {
    'USD: CMS:2Y': '2y',
    'USD: CMS:5Y': '5y',
    'USD: CMS:10Y': '10y'
}

# 创建upper_bound和lower_bound的映射关系
# 并将映射关系中的值乘以100，统一数量级以便比较
bound_info = trade_info.drop_duplicates('underlying').set_index('underlying') \
    [['upper_bound', 'lower_bound']].apply(lambda x: x * 100).to_dict('index')

# 根据underlying生成三个新的数据集
for underlying, tenor in underlying_to_tenor.items():
    filtered_cms_data = CMS_data[CMS_data['Tenor'] == tenor]
    underlying_swap_rate = f"swap-rates-{tenor}.csv"
    filtered_cms_data.to_csv(underlying_swap_rate, index=False)
    print(f"Saved {underlying_swap_rate}")

# 统计特征：CMS平均值/标准差/最大值/最小值
# 时间序列特征：利差计算：日/周/月利差的STD
# bound特征：利率范围内的时间比例
# 定义操作函数
def process_market_data(df, upper_bound, lower_bound):
    # 转换日期格式并排序
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    df = df.sort_values(by='Start Date')

    # 平均处理重复的Start Date
    df = df.groupby('Start Date').agg({'Swap Rate': 'mean'}).reset_index()

    # 填充缺失日期并插值
    full_date_range = pd.date_range(start=df['Start Date'].min(), end=df['Start Date'].max(), freq='D')
    df = df.set_index('Start Date').reindex(full_date_range).rename_axis('Start Date').reset_index()
    df['Swap Rate'] = df['Swap Rate'].interpolate()

    # 计算差分
    df['Daily Diff'] = df['Swap Rate'].diff()
    df['Weekly Diff'] = df['Swap Rate'].diff(7)
    df['Monthly Diff'] = df['Swap Rate'].diff(30)

    # 计算差分的标准差并只保留标准差的值
    daily_diff_std = df['Daily Diff'].std()
    weekly_diff_std = df['Weekly Diff'].std()
    monthly_diff_std = df['Monthly Diff'].std()

    # 计算均值、最大值、最小值等统计特征
    mean_cms = df['Swap Rate'].mean()
    std_cms = df['Swap Rate'].std()
    max_cms = df['Swap Rate'].max()
    min_cms = df['Swap Rate'].min()

    # 计算利率范围内的时间比例
    df['Within Range'] = (df['Swap Rate'] >= lower_bound) & (df['Swap Rate'] <= upper_bound)
    proportion_within_range = df['Within Range'].mean()

    return (daily_diff_std, weekly_diff_std, monthly_diff_std,
            mean_cms, std_cms, max_cms, min_cms,
            proportion_within_range)


# 初始化一个空的列表来存储所有数据
final_results = []

# 对每个子数据文件进行处理
for underlying, tenor in underlying_to_tenor.items():
    input_filename = f"swap-rates-{tenor}.csv"
    df = pd.read_csv(input_filename)

    # 获取upper_bound和lower_bound
    upper_bound = bound_info[underlying]['upper_bound']
    lower_bound = bound_info[underlying]['lower_bound']

    # 处理市场数据并计算统计特征和时间比例
    daily_diff_std, weekly_diff_std, monthly_diff_std, \
        mean_cms, std_cms, max_cms, min_cms, \
        proportion_within_range \
        = process_market_data(df, upper_bound, lower_bound)

    # 将结果添加到结果列表中
    final_results.append(
        {'Underlying': underlying,
         'Daily_Diff_STD': daily_diff_std,
         'Weekly_Diff_STD': weekly_diff_std,
         'Monthly_Diff_STD': monthly_diff_std,
         'Mean_CMS': mean_cms,
         'STD_CMS': std_cms,
         'Max_CMS': max_cms,
         'Min_CMS': min_cms,
         'Proportion_Within_Range': proportion_within_range})

# 将所有结果转换为DataFrame
final_df = pd.DataFrame(final_results)

# 将最终的DataFrame写入CSV文件
final_df.to_csv("final_results.csv", index=False)

# 合并数据到trade-information.csv
final_result = pd.read_csv("final_results.csv")
merged_df = pd.merge(trade_info, final_result, how='left', left_on='underlying', right_on='Underlying')

# 删除 'Underlying' 列
merged_df.drop(columns=['Underlying'], inplace=True)

# 删除 'underlying' 列
merged_df.drop(columns=['underlying'], inplace=True)

# 将合并后的DataFrame写入CSV文件
merged_df.to_csv("final_feature_results.csv", index=False)

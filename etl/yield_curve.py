import os
import json
import time
import requests
import pandas as pd
from tqdm import tqdm


url = "https://yield.chinabond.com.cn/cbweb-czb-web/czb/historyQuery"
data_path = 'data'

# 定义请求头
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Host": "yield.chinabond.com.cn",
    "Origin": "https://yield.chinabond.com.cn",
    "Referer": "https://yield.chinabond.com.cn/cbweb-czb-web/czb/showHistory?locale=cn_ZH&nameType=1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows"
}

origin_df = pd.read_csv(os.path.join(data_path, 'yield.csv'))
past_year = int(origin_df['workTime'].max()[:4])
this_year = time.localtime().tm_year
# 结果列表
results = []
# 从2000年开始，按年循环
for year in tqdm(range(past_year, this_year + 1)):  # 假设我们只请求到2024年
    # 设置请求的查询参数
    params = {
        "startDate": f"{year}-01-01",
        "endDate": f"{year}-12-31",
        "gjqx": "0",
        "locale": "cn_ZH",
        "qxmc": "1"
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, params=params)
    # 检查请求是否成功
    if response.status_code == 200:
        # 将响应内容解析为JSON
        try:
            data = response.json()
            # 将解析后的数据添加到结果列表中
            results.append(data)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from response for year {year}")
    else:
        print(f"Failed to get data for year {year}, status code: {response.status_code}")
    time.sleep(1)

print(f"Total years of data collected: {len(results)}")
real_data_list = []
for item in results:
    if item['heList']:
        real_data_list = real_data_list + item['heList']
new_df = pd.DataFrame(real_data_list).sort_values(by='workTime')
total_df = pd.concat([origin_df, new_df], axis=0)
total_df = total_df.drop_duplicates()
total_df.to_csv(os.path.join(data_path, 'yield.csv'), index=False)
import os
import datetime
import pandas as pd
import tushare as ts
end_date = datetime.datetime.now().strftime('%Y%m%d')
tushare_token = os.getenv('TUSHARE_TOKEN')  # 存储在github的秘钥仓库中，供action每天运行
pro = ts.pro_api(tushare_token)
data_path = 'data'

# reference: https://tushare.pro/document/2?doc_id=25
#查询当前所有正常上市交易的股票列表
list_df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,delist_date')
list_df['status'] = 'L'
#查询已经退市或暂停上市的股票列表
exit_df = pro.stock_basic(exchange='', list_status='D', fields='ts_code,symbol,name,area,industry,list_date,delist_date')
exit_df['status'] = 'D'
# 查询暂停上市的股票
stop_df = pro.stock_basic(exchange='', list_status='P', fields='ts_code,symbol,name,area,industry,list_date,delist_date')
stop_df['status'] = 'P'
total_stock_df = pd.concat([list_df, exit_df, stop_df], axis=0)
total_stock_df.to_csv(os.path.join(data_path, 'stock_basic.csv'), index=False)

# reference: https://tushare.pro/document/2?doc_id=95
index_list = ['000001.SH', '399001.SZ', '000016.SH', '000300.SH', '000905.SH', '000852.SH']
index_df = pd.DataFrame()
for i in index_list:
    tmp_df = pro.index_daily(ts_code=i, start_date='19900101', end_date=end_date)
    index_df = pd.concat([index_df, tmp_df], axis=0)
index_df.to_csv(os.path.join(data_path, 'stock_index.csv'), index=False)

# reference: https://tushare.pro/document/2?doc_id=189
tf_list = ['TS.CFX', 'TF.CFX', 'T.CFX', 'TL.CFX']  # 2Y 5Y 10Y 30Y
tf_df = pd.DataFrame()
for i in tf_list:
    tmp_df = pro.fut_mapping(ts_code=i)
    tf_df = pd.concat([tf_df, tmp_df], axis=0)
tf_df.to_csv(os.path.join(data_path, 'tf_continuous.csv'), index=False)

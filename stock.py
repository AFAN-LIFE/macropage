import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt


class StockMarket:
    def __init__(self):
        self.stock_basic_df = pd.read_csv('data/stock_basic.csv')
        self.stock_index_df = pd.read_csv('data/stock_index.csv')

    # TODO 修改为蜡烛图：https://altair-viz.github.io/gallery/candlestick_chart.html
    def sh_index_plot(self):
        index_df = self.stock_index_df[self.stock_index_df['ts_code'] == '000001.SH'].sort_values(
            by='trade_date').set_index('trade_date')
        index_df.index = index_df.index.astype(str)
        index_df['amount'] = index_df['amount'] / 1e5  # 千元 -> 亿元
        options = index_df.index.tolist()
        date = st.select_slider("请选择想要查询的日期", options=options, value=options[-240], key='sh_index_plot')
        st.write("当前选择的起始日期是：", date)
        pro_df = index_df.loc[date:, :].reset_index()
        bars = alt.Chart(pro_df).mark_bar().encode(
            x='trade_date',
            y='amount'
        )
        line = alt.Chart(pro_df).mark_line(color='red').encode(
            x='trade_date',
            y='close'
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(line, bars).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)

    def sz_index_plot(self):
        index_df = self.stock_index_df[self.stock_index_df['ts_code'] == '399001.SZ'].sort_values(
            by='trade_date').set_index('trade_date')
        index_df.index = index_df.index.astype(str)
        index_df['amount'] = index_df['amount'] / 1e5  # 千元 -> 亿元
        options = index_df.index.tolist()
        date = st.select_slider("请选择想要查询的日期", options=options, value=options[-240], key='sz_index_plot')
        st.write("当前选择的起始日期是：", date)
        pro_df = index_df.loc[date:, :].reset_index()
        bars = alt.Chart(pro_df).mark_bar().encode(
            x='trade_date',
            y='amount'
        )
        line = alt.Chart(pro_df).mark_line(color='red').encode(
            x='trade_date',
            y='close'
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(line, bars).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)

    def list_delist_plot(self):
        # 按照月度聚合
        stock_df = self.stock_basic_df.copy()
        stock_df = stock_df[stock_df['ts_code'].apply(lambda x: ('SH' in x) or ('SZ' in x))]  # 仅保留沪深
        stock_df['list_year'] = stock_df['list_date'].apply(lambda x: str(x)[:4])
        stock_df['list_month'] = stock_df['list_date'].apply(lambda x: str(x)[4:6])
        stock_df['delist_year'] = stock_df['delist_date'].apply(lambda x: np.nan if str(x) == 'nan' else str(x)[:4])
        stock_df['delist_month'] = stock_df['delist_date'].apply(lambda x: np.nan if str(x) == 'nan' else str(x)[4:6])
        list_group_se = stock_df.groupby(['list_year', 'list_month'])['ts_code'].count().sort_index()
        delist_group_se = stock_df.groupby(['delist_year', 'delist_month'])['ts_code'].count().sort_index()
        list_delist_df = pd.concat([list_group_se, delist_group_se], axis=1)
        list_delist_df.columns = ['上市', '退市']
        list_delist_df = list_delist_df.reset_index()
        list_delist_df['date'] = list_delist_df.apply(lambda x: f'{x.iloc[0]}{x.iloc[1]}', axis=1)
        list_delist_df = list_delist_df.set_index('date').loc[:, ['上市', '退市']].sort_index()
        options = list_delist_df.index.tolist()
        date = st.select_slider("请选择想要查询的日期", options=options, value=options[-24], key='list_delist_plot')
        st.write("当前选择的起始日期是：", date)
        pro_df = list_delist_df.loc[date:, :].reset_index()
        # 使用Altair创建柱状图
        bar1 = alt.Chart(pro_df).mark_bar().encode(
            x=alt.X('date:O', title='Date'),
            y=alt.Y('上市:Q', title='上市'),
            xOffset='variable:N'
        ).transform_calculate(
            variable='"上市"'
        )

        bar2 = alt.Chart(pro_df).mark_bar(color='red').encode(
            x=alt.X('date:O', title='Date'),
            y=alt.Y('退市:Q', title='退市'),
            xOffset='variable:N'
        ).transform_calculate(
            variable='"退市"'
        )

        # 将柱状图和折线图组合在一起
        chart = alt.layer(bar1, bar2).resolve_scale(
            y='independent'
        )
        st.altair_chart(chart, use_container_width=True)

    def list_index_plot(self):
        # 构建出大盘指数每月最后一天的收盘价
        index_df = self.stock_index_df[self.stock_index_df['ts_code'] == '000001.SH'].sort_values(
            by='trade_date')
        index_df['month'] = index_df['trade_date'].astype(str).apply(lambda x: x[:6])
        month_index_df = index_df.drop_duplicates(subset='month', keep='last')
        month_index_df = month_index_df.set_index('month')['close']
        # 构建每月上市的股票数量
        stock_df = self.stock_basic_df.copy()
        stock_df = stock_df[stock_df['ts_code'].apply(lambda x: ('SH' in x) or ('SZ' in x))]  # 仅保留沪深
        stock_df['list_year'] = stock_df['list_date'].apply(lambda x: str(x)[:4])
        stock_df['list_month'] = stock_df['list_date'].apply(lambda x: str(x)[4:6])
        list_group_se = stock_df.groupby(['list_year', 'list_month'])['ts_code'].count().sort_index()
        list_group_df = list_group_se.reset_index()
        list_group_df['month'] = list_group_df.apply(lambda x: f'{x.iloc[0]}{x.iloc[1]}', axis=1)
        list_group_df = list_group_df.set_index('month').iloc[:, 2].sort_index()
        # 合并展示
        merge_df = pd.concat([month_index_df, list_group_df], axis=1).sort_index()
        merge_df.columns = ['上证指数', '上市数量']
        options = merge_df.index.tolist()
        date = st.select_slider("请选择想要查询的日期", options=options, value=options[-24], key='list_index_plot')
        st.write("当前选择的起始日期是：", date)
        pro_df = merge_df.loc[date:, :].reset_index()
        bars = alt.Chart(pro_df).mark_bar().encode(
            x='month',
            y='上市数量'
        )
        line = alt.Chart(pro_df).mark_line(color='red').encode(
            x='month',
            y='上证指数'
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(line, bars).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)


def stock_market_analysis():
    stock_market = StockMarket()
    st.title('上证指数走势图')
    st.write('单位：特殊单位/亿元@日')
    stock_market.sh_index_plot()
    st.title('深圳成指走势图')
    st.write('单位：特殊单位/亿元@日')
    stock_market.sz_index_plot()
    st.title('每月上市/退市情况')
    st.write('单位：个数@日')
    stock_market.list_delist_plot()
    st.title('每月上证指数和上市数量')
    st.write('单位：特殊单位/个数@日')
    stock_market.list_index_plot()
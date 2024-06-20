import re
import time
import datetime
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from tool import preprocess_choice_data, get_choice_unit_arr


# 数据的列名不要有太多的:，不然会报错： If you are trying to use a column name that contains a colon, prefix it with a backslash; for example "column\:name" instead of "column:name".

class GDP:
    def __init__(self):
        df = preprocess_choice_data('data/GDP.xlsx')
        df = df[(df['指标名称'] >= '1992-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        df['月份'] = [i[-2:] for i in df.index]
        df['年份'] = [i[:4] for i in df.index]
        self.df = df

    def total_plot(self):
        pro_df = self.df.loc[:, ['中国:GDP:不变价:累计同比']]
        pro_df.columns = [i.replace('中国:', '').replace(':', '-') for i in pro_df.columns]
        st.line_chart(pro_df)

    def produce_proportion(self):
        pro_df = self.df[self.df['月份'] == '12']
        pro_df = pro_df.loc[:,
                 ['中国:GDP:现价:第一产业:累计值', '中国:GDP:现价:第二产业:累计值', '中国:GDP:现价:第三产业:累计值']]
        pro_df = pro_df.div(pro_df.sum(axis=1).replace(0, np.nan), axis=0)
        pro_df.columns = [i.replace('中国:', '').replace(':', '-') for i in pro_df.columns]
        st.bar_chart(pro_df)

    def produce_change(self):
        pro_df = self.df[self.df['月份'] == '12']
        pro_df = pro_df.loc[:, ['中国:GDP:不变价:第一产业:当季同比', '中国:GDP:不变价:第二产业:当季同比',
                                '中国:GDP:不变价:第三产业:当季同比']]
        pro_df.columns = [i.replace('中国:', '').replace(':', '-') for i in pro_df.columns]
        st.line_chart(pro_df)

    def produce_contribute(self):
        pro_df = self.df[self.df['月份'] == '12']
        pro_df = pro_df.loc[:,
                 ['中国:GDP增长贡献率:第一产业', '中国:GDP增长贡献率:第二产业', '中国:GDP增长贡献率:第三产业']]
        pro_df.columns = [i.replace('中国:', '').replace(':', '-') for i in pro_df.columns]
        st.bar_chart(pro_df)

    def produce_stimulation(self):
        pro_df = self.df[self.df['月份'] == '12']
        pro_df = pro_df.loc['1992':,
                 ['中国:对GDP增长的拉动:第一产业', '中国:对GDP增长的拉动:第二产业', '中国:对GDP增长的拉动:第三产业']]
        pro_df.columns = [i.replace('中国:', '').replace(':', '-') for i in pro_df.columns]
        st.bar_chart(pro_df)

    def revenue_proportion(self):
        pro_df = self.df[self.df['月份'] == '12']
        pro_df = pro_df.loc[:, ['中国:GDP:最终消费支出', '中国:GDP:资本形成总额', '中国:GDP:货物和服务净出口']]
        pro_df = pro_df.div(pro_df.sum(axis=1).replace(0, np.nan), axis=0)
        pro_df.columns = [i.replace('中国:', '').replace(':', '-') for i in pro_df.columns]
        st.bar_chart(pro_df)

    def revenue_contribute(self):
        pro_df = self.df[self.df['月份'] == '12']
        pro_df = pro_df.loc[:, ['中国:三大需求对GDP增长的贡献率:最终消费支出:累计值',
                                '中国:三大需求对GDP增长的贡献率:资本形成总额:累计值',
                                '中国:三大需求对GDP增长的贡献率:货物和服务净出口:累计值']]
        pro_df.columns = [i.replace('中国:三大需求对GDP增长的贡献率:', '').replace(':', '-') for i in pro_df.columns]
        st.line_chart(pro_df.dropna())


class PMI:
    def __init__(self):
        df = preprocess_choice_data('data/PMI.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        self.df = df

    def total_plot(self):
        pro_df = self.df.loc[:, ['PMI', '非制造业PMI:商务活动', '综合PMI:产出指数']]
        start_date = '2019-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df)

    def demand_plot(self):
        pro_df = self.df.loc[:, ['PMI:新订单', 'PMI:新出口订单', 'PMI:积压订单']]
        start_date = '2019-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df)

    def produce_plot(self):
        pro_df = self.df.loc[:, ['PMI:新订单', 'PMI:生产']]
        start_date = '2019-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df)

    def procurement_plot(self):
        pro_df = self.df.loc[:, ['PMI:采购量', 'PMI:进口']]
        start_date = '2019-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df)

    def inventory_plot(self):
        pro_df = self.df.loc[:, ['PMI:产成品库存', 'PMI:原材料库存']]
        start_date = '2019-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df)

    def price_plot(self):
        pro_df = self.df.loc[:, ['PMI:购进价格', 'PMI:出厂价格']]
        start_date = '2019-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df)


class CPI_PPI:
    def __init__(self):
        df = preprocess_choice_data('data/CPI+PPI.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        self.df = df

    def total_plot(self):
        pro_df = self.df.loc[:, ['CPI:环比', 'PPI:全部工业品:环比']]
        start_date = '2000-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df.astype(float))

    def cpi_plot(self):
        pro_df = self.df.loc[:, ['CPI:环比', 'CPI:食品:环比', 'CPI:非食品:环比']]
        start_date = '2000-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df.astype(float))

    def ppi_plot(self):
        pro_df = self.df.loc[:, ['PPI:全部工业品:环比', 'PPI:生产资料:环比', 'PPI:生活资料:环比']]
        start_date = '2000-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df.astype(float))


class TRSCG:
    def __init__(self):
        df = preprocess_choice_data('data/社零.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        rate_df = df.pct_change(10)
        rate_df.columns = [i + '%' for i in rate_df.columns]
        df = pd.concat([df, rate_df], axis=1)
        self.df = df

    def total_plot(self):
        pro_df = self.df.loc[:, ['社会消费品零售总额:当月值', '社会消费品零售总额:当月值%']].reset_index()
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        start_date = '2000-01'
        pro_df = pro_df.loc[start_date:, :]
        bars = alt.Chart(pro_df).mark_bar().encode(
            x='指标名称',
            y='社会消费品零售总额-当月值'
        )
        line = alt.Chart(pro_df).mark_line(color='red').encode(
            x='指标名称',
            y='社会消费品零售总额-当月值%'
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(bars, line).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)

    def season_plot(self):
        start_date = '2019-01'
        pro_df = self.df.loc[start_date:, ['社会消费品零售总额:当月值']]
        pro_df['月份'] = [i[-2:] for i in pro_df.index]
        pro_df['年份'] = [i[:4] for i in pro_df.index]
        pro_df = pro_df.pivot(index=['月份'], columns=['年份'], values='社会消费品零售总额:当月值')
        st.line_chart(pro_df.astype(float))

    def automobile_proportion(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:,
                 ['社会消费品零售总额:当月值', '社会消费品零售总额:除汽车以外的消费品零售额:当月值']]
        pro_df.columns = ['总额', '除汽车']
        pro_df = pro_df.div(pro_df['总额'], axis=0)
        pro_df['汽车'] = pro_df['总额'] - pro_df['除汽车']
        st.bar_chart(pro_df.iloc[:, 1:].astype(float))

    def automobile_increase(self):
        start_date = '2000-01'
        pro_df = self.df.loc[:, ['社会消费品零售总额:当月值', '社会消费品零售总额:除汽车以外的消费品零售额:当月值']]
        pro_df.columns = ['总额', '除汽车']
        pro_df['汽车'] = pro_df['总额'] - pro_df['除汽车']
        pro_df = pro_df.pct_change(10).loc[start_date:]
        st.line_chart(pro_df.astype(float))

    def goods_food_proportion(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['社会消费品零售总额:商品零售:当月值', '社会消费品零售总额:餐饮收入:当月值']]
        pro_df.columns = ['商品零售', '餐饮收入']
        pro_df = pro_df.div(pro_df.sum(axis=1), axis=0)
        st.bar_chart(pro_df.astype(float))

    def goods_food_increase(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['社会消费品零售总额:当月值%', '社会消费品零售总额:商品零售:当月值%',
                                           '社会消费品零售总额:餐饮收入:当月值%']]
        pro_df.columns = ['总额', '商品零售', '餐饮收入']
        st.line_chart(pro_df.astype(float))

    def area_proportion(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['社会消费品零售总额:城镇:当月值', '社会消费品零售总额:农村:当月值']]
        pro_df.columns = ['城镇', '农村']
        pro_df = pro_df.div(pro_df.sum(axis=1).replace(0, np.nan), axis=0)
        st.bar_chart(pro_df.astype(float))

    def area_increase(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:,
                 ['社会消费品零售总额:当月值%', '社会消费品零售总额:城镇:当月值%', '社会消费品零售总额:农村:当月值%']]
        pro_df.columns = ['总额', '城镇', '农村']
        st.line_chart(pro_df.astype(float))

    def online_proportion(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['社会消费品零售总额:当月值', '社会消费品零售总额:网上零售:当月值']]
        pro_df.columns = ['总额', '网上零售']
        pro_df = pro_df.div(pro_df['总额'].replace(0, np.nan), axis=0)
        pro_df['网下零售'] = pro_df['总额'] - pro_df['网上零售']
        st.bar_chart(pro_df.iloc[:, 1:].astype(float))

    def online_increase(self):
        start_date = '2000-01'
        pro_df = self.df.loc[:, ['社会消费品零售总额:当月值', '社会消费品零售总额:网上零售:当月值']]
        pro_df.columns = ['总额', '网上零售']
        pro_df['网下零售'] = pro_df['总额'] - pro_df['网上零售']
        pro_df = pro_df.pct_change(10).loc[start_date:]
        st.line_chart(pro_df.astype(float))

    def limit_proportion(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['社会消费品零售总额:当月值', '限额以上企业消费品零售总额:当月值']]
        pro_df.columns = ['总额', '限额']
        pro_df = pro_df.div(pro_df['总额'].replace(0, np.nan), axis=0)
        pro_df['非限额'] = pro_df['总额'] - pro_df['限额']
        st.bar_chart(pro_df.iloc[:, 1:].astype(float))

    def limit_increase(self):
        start_date = '2000-01'
        pro_df = self.df.loc[:, ['社会消费品零售总额:当月值', '限额以上企业消费品零售总额:当月值']]
        pro_df.columns = ['总额', '限额']
        pro_df['非限额'] = pro_df['总额'] - pro_df['限额']
        pro_df = pro_df.pct_change(10).loc[start_date:]
        st.line_chart(pro_df.astype(float))


class ExportBasic:
    def __init__(self):
        df = preprocess_choice_data('data/进出口基本.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        self.df = df

    def total_plot(self):
        start_date = '2013-01'
        pro_df = self.df.loc[start_date:,
                 ['出口金额:当月同比', '进口金额:当月同比', '出口金额:人民币:当月同比', '进口金额:人民币:当月同比']]
        st.line_chart(pro_df.dropna().astype(float))

    def amount_plot(self):
        start_date = '2013-01'
        pro_df = self.df.loc[start_date:,
                 ['出口金额:当月值', '进口金额:当月值', '进出口金额:当月值', '贸易顺差:当月值']].astype(float)
        pro_df['进出口金额:当月值'] = pro_df['进出口金额:当月值']
        st.line_chart(pro_df)

    def output_season_plot(self):
        start_date = '2019-01'
        pro_df = self.df.loc[start_date:, ['出口金额:当月同比']]
        pro_df['月份'] = [i[-2:] for i in pro_df.index]
        pro_df['年份'] = [i[:4] for i in pro_df.index]
        pro_df = pro_df.pivot(index=['月份'], columns=['年份'], values='出口金额:当月同比')
        st.line_chart(pro_df)

    def input_season_plot(self):
        start_date = '2019-01'
        pro_df = self.df.loc[start_date:, ['进口金额:当月同比']]
        pro_df['月份'] = [i[-2:] for i in pro_df.index]
        pro_df['年份'] = [i[:4] for i in pro_df.index]
        pro_df = pro_df.pivot(index=['月份'], columns=['年份'], values='进口金额:当月同比')
        st.line_chart(pro_df)


class ExportCountry:
    def __init__(self):
        path = 'data/进出口区域.xlsx'
        df = preprocess_choice_data(path)
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        input_df = df.loc[:, df.columns.str.contains('进口')]
        input_df.columns = [i.split(':')[0] for i in input_df.columns]
        output_df = df.loc[:, df.columns.str.contains('出口')]
        output_df.columns = [i.split(':')[0] for i in output_df.columns]
        self.input_df = input_df
        self.output_df = output_df

    def output_portion(self):
        options = self.output_df.index.tolist()
        date = st.select_slider("请选择想要查询的日期", options=options, key='output_portion')
        st.write("当前选择的日期是：", date)
        # 创建2个空的容器
        slider_container = st.empty()
        chart_container = st.empty()
        run = st.button("播放动画", key='output_run', type='primary')
        def run_plot(date, object):
            selected_df = self.output_df.loc[date].reset_index()
            chart1 = alt.Chart(selected_df).mark_arc().encode(
                theta=alt.Theta(field=selected_df.columns[1], type="quantitative"),
                color=alt.Color(field=selected_df.columns[0], type="nominal"),
            )
            object.altair_chart(chart1, theme="streamlit", use_container_width=True)
        if run:
            for i in options:
                time.sleep(0.1)
                slider_container.select_slider("Select Date", options=options, value=i, key=i)
                run_plot(i, chart_container)
        else:
            run_plot(date, st)

    def input_portion(self):
        options = self.input_df.index.tolist()
        date = st.select_slider("请选择想要查询的日期", options=options, key='input_portion')
        st.write("当前选择的日期是：", date)
        # 创建2个空的容器
        slider_container = st.empty()
        chart_container = st.empty()
        run = st.button("播放动画", key='input_run', type='primary')
        def run_plot(date, object):
            selected_df = self.input_df.loc[date].reset_index()
            chart2 = alt.Chart(selected_df).mark_arc().encode(
                theta=alt.Theta(field=selected_df.columns[1], type="quantitative"),
                color=alt.Color(field=selected_df.columns[0], type="nominal"),
            )
            object.altair_chart(chart2, theme="streamlit", use_container_width=True)
        if run:
            for i in options:
                time.sleep(0.1)
                slider_container.select_slider("Select Date", options=options, value=i, key=i)
                run_plot(i, chart_container)
        else:
            run_plot(date, st)

    def output_trend(self):
        start_date = '2000-01'
        plot_df = self.output_df
        plot_df['年份'] = [i[:4] for i in plot_df.index]
        plot_df = plot_df.groupby(['年份']).sum()
        plot_df = plot_df.div(plot_df.sum(axis=1), axis=0)
        plot_df = plot_df.loc[start_date:, plot_df.iloc[0].sort_values().tail(5).index]
        st.line_chart(plot_df.dropna().astype(float) * 100)

    def input_trend(self):
        start_date = '2000-01'
        plot_df = self.input_df
        plot_df['年份'] = [i[:4] for i in plot_df.index]
        plot_df = plot_df.groupby(['年份']).sum()
        plot_df = plot_df.div(plot_df.sum(axis=1), axis=0)
        plot_df = plot_df.loc[start_date:, plot_df.iloc[0].sort_values().tail(5).index]
        st.line_chart(plot_df.dropna().astype(float) * 100)


class FixedAssetInvest:
    def __init__(self):
        df = preprocess_choice_data('data/固定资产投资.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        self.df = df

    def total_plot(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='fixed_asset_total_plot')
        pro_df = self.df.loc[start_date:, :]
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:, ['固定资产投资完成额:累计值', '固定资产投资完成额:累计同比']].reset_index()
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        bars = alt.Chart(pro_df).mark_bar().encode(
            x='指标名称',
            y='固定资产投资完成额-累计值'
        )
        line = alt.Chart(pro_df).mark_line(color='red').encode(
            x='指标名称',
            y='固定资产投资完成额-累计同比'
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(bars, line).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)

    def season_plot(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['固定资产投资完成额:累计同比']]
        pro_df['月份'] = [i[-2:] for i in pro_df.index]
        pro_df['年份'] = [i[:4] for i in pro_df.index]
        pro_df = pro_df.pivot(index=['月份'], columns=['年份'], values='固定资产投资完成额:累计同比')
        print(pro_df)
        pro_df = pro_df.astype(float)
        st.line_chart(pro_df)

    def construct_type(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='construct_type')
        pro_df = self.df.loc[start_date:, :]
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:, ['固定资产投资完成额:新建:累计同比', '固定资产投资完成额:扩建:累计同比',
                                '固定资产投资完成额:改建:累计同比']]
        pro_df.columns = ['新建', '扩建', '改建']
        pro_df = pro_df.astype(float)
        st.line_chart(pro_df)

    def portion(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='portion')
        pro_df = self.df.loc[start_date:, :]
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:,
                 ['固定资产投资完成额:建筑安装工程:累计同比', '固定资产投资完成额:设备工器具购置:累计同比',
                  '固定资产投资完成额:其他费用:累计同比']]
        pro_df.columns = ['建筑安装工程', '设备工器具购置', '其他费用']
        pro_df = pro_df.astype(float)
        st.line_chart(pro_df)

    def industry(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='industry')
        pro_df = self.df.loc[start_date:, :]
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:, ['固定资产投资完成额:第一产业:累计同比', '固定资产投资完成额:第二产业:累计同比',
                                '固定资产投资完成额:第三产业:累计同比']]
        pro_df.columns = ['第一产业', '第二产业', '第三产业']
        pro_df = pro_df.astype(float)
        st.line_chart(pro_df)

    def state_owned(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='state_owned')
        pro_df = self.df.loc[start_date:, :]
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:, ['民间固定资产投资完成额:累计同比', '固定资产投资完成额:国有控股企业:累计同比']]
        pro_df.columns = ['民间', '国有控股企业']
        pro_df = pro_df.astype(float)
        st.line_chart(pro_df)


class FinancingMoney:
    def __init__(self):
        df = preprocess_choice_data('data/社融货币.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        df['社融增量:同比增速'] = df['社会融资增量:当月值'].pct_change(12)
        df['社融存量:同比增速'] = df['社会融资规模存量'].pct_change(12)
        self.df = df

    def financing_plot(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['社会融资增量:当月值', '社融增量:同比增速']].reset_index()
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        bars = alt.Chart(pro_df).mark_bar().encode(
            x='指标名称',
            y='社会融资增量-当月值'
        )
        line = alt.Chart(pro_df).mark_line(color='red').encode(
            x='指标名称',
            y='社融增量-同比增速'
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(bars, line).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)

    def season_plot(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['社会融资增量:当月值']]
        pro_df['月份'] = [i[-2:] for i in pro_df.index]
        pro_df['年份'] = [i[:4] for i in pro_df.index]
        pro_df = pro_df.pivot(index=['月份'], columns=['年份'], values='社会融资增量:当月值')
        pro_df = pro_df.astype(float)
        st.line_chart(pro_df)

    def financing_portion(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:,
                 ['社会融资增量:新增人民币贷款:当月值', '社会融资增量:新增外币贷款(按人民币计):当月值',
                  '社会融资增量:新增委托贷款:当月值', '社会融资增量:新增信托贷款:当月值',
                  '社会融资增量:新增未贴现银行承兑汇票:当月值',
                  '社会融资增量:企业债券融资:当月值', '社会融资增量:非金融企业境内股票融资:当月值',
                  '社会融资增量:政府债券:当月值', '社会融资增量:贷款核销:当月值',
                  '社会融资增量:存款类金融机构资产支持证券:当月值',
                  ]]
        pro_df.columns = ['人民币贷款', '外币贷款', '委托贷款', '信托贷款', '未贴现银行承兑汇票', '企业债券融资',
                          '企业股票融资', '政府债券', '贷款核销', '存款机构ABS']
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def increment_loan(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:,
                 ['金融机构:新增人民币贷款:居民户:短期:当月值', '金融机构:新增人民币贷款:居民户:中长期:当月值',
                  '金融机构:新增人民币贷款:非金融性公司及其他部门:短期:当月值',
                  '金融机构:新增人民币贷款:非金融性公司及其他部门:中长期:当月值',
                  '金融机构:新增人民币贷款:非金融性公司及其他部门:票据融资:当月值',
                  ]]
        pro_df.columns = ['居民户:短期', '居民户:中长期', '企业:短期', '企业:中长期', '企业:票据融资', ]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def off_sheet(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:,
                 ['社会融资增量:新增委托贷款:当月值', '社会融资增量:新增信托贷款:当月值', ]]
        pro_df.columns = ['新增委托贷款', '新增信托贷款']
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def direct_financing(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:,
                 ['社会融资增量:企业债券融资:当月值', '社会融资增量:非金融企业境内股票融资:当月值']]
        pro_df.columns = ['企业债券融资', '企业股票融资']
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def financing_other(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:,
                 ['社会融资增量:政府债券:当月值', '社会融资增量:贷款核销:当月值',
                  '社会融资增量:存款类金融机构资产支持证券:当月值']]
        pro_df.columns = ['政府债券', '贷款核销', '存款机构ABS']
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def money_plot(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:,
                 ['M0:同比', 'M1:同比', 'M2:同比']]
        pro_df.columns = ['政府债券', '贷款核销', '存款机构ABS']
        st.line_chart(pro_df.dropna().astype(float))

    def money_scissors(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df['M1-M2增速'] = pro_df['M1:同比'] - pro_df['M2:同比']
        pro_df['社融-M2增速'] = pro_df['社融存量:同比增速'] * 100 - pro_df['M2:同比']
        pro_df = pro_df.loc[:, ['M1-M2增速', '社融-M2增速']]
        st.line_chart(pro_df.dropna().astype(float))


class Fiscal:
    def __init__(self):
        df = preprocess_choice_data('data/财政.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        self.df = df

    def central_budget_revenue(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='central_budget_revenue')
        pro_df = self.df.loc[start_date:, :]
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:, ['一般公共预算收入:中央财政:累计值', '一般公共预算收入:地方财政:累计值']]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def tax_budget_revenue(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='tax_budget_revenue')
        pro_df = self.df.loc[start_date:, :]
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:, ['一般公共预算收入:税收收入:累计值', '一般公共预算收入:非税收入:累计值']]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def tax_detail_revenue(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='tax_detail_revenue')
        pro_df = self.df.loc[start_date:, :]
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:, ['一般公共预算收入:税收收入:增值税:累计值', '一般公共预算收入:税收收入:消费税:累计值',
                                '一般公共预算收入:税收收入:海关代征增值税和消费税:累计值',
                                '一般公共预算收入:税收收入:外贸企业出口退税:累计值',
                                '一般公共预算收入:税收收入:营业税:累计值',
                                '一般公共预算收入:税收收入:企业所得税:累计值',
                                '一般公共预算收入:税收收入:个人所得税:累计值',
                                '一般公共预算收入:税收收入:资源税:累计值',
                                '一般公共预算收入:税收收入:城市维护建设税:累计值',
                                '一般公共预算收入:税收收入:房产税:累计值',
                                '一般公共预算收入:税收收入:印花税:累计值',
                                '一般公共预算收入:税收收入:证券交易印花税:累计值',
                                '一般公共预算收入:税收收入:城镇土地使用税:累计值',
                                '一般公共预算收入:税收收入:土地增值税:累计值',
                                '一般公共预算收入:税收收入:车辆购置税:累计值', '一般公共预算收入:税收收入:关税:累计值',
                                '一般公共预算收入:税收收入:契税:累计值']]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def central_budget_expenditure(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='central_budget_expenditure')
        pro_df = self.df.loc[start_date:, :]
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:, ['一般公共预算支出:中央财政:累计值', '一般公共预算支出:地方财政:累计值']]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def total_detail_expenditure(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='total_detail_expenditure')
        pro_df = self.df.loc[start_date:, :]
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:,
                 ['一般公共预算支出:一般公共服务:累计值', '一般公共预算支出:教育:累计值',
                  '一般公共预算支出:科学技术:累计值',
                  '一般公共预算支出:文化体育与传媒:累计值', '一般公共预算支出:社会保障和就业:累计值',
                  '一般公共预算支出:卫生健康:累计值',
                  '一般公共预算支出:节能环保:累计值', '一般公共预算支出:城乡社区事务:累计值',
                  '一般公共预算支出:农林水事务:累计值',
                  '一般公共预算支出:交通运输:累计值', ]]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def budget_deficit(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='budget_deficit')
        pro_df = self.df.loc[start_date:, :]
        pro_df['预算赤字'] = pro_df['一般公共预算支出:累计值'] - pro_df['一般公共预算收入:累计值']
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:, ['预算赤字']]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def government_fund(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='government_fund')
        pro_df = self.df.loc[start_date:, :]
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:, ['中央政府性基金收入:累计值', '地方政府性基金本级收入:累计值']]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def land_grand_fee(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='land_grand_fee')
        pro_df = self.df.loc[start_date:, :]
        pro_df['其他基金收入'] = pro_df['全国政府性基金收入:累计值'] - pro_df['国有土地使用权出让收入:累计值']
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[:, ['其他基金收入', '国有土地使用权出让收入:累计值']]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)


class PopulationEnployment:
    def __init__(self):
        df = preprocess_choice_data('data/人口就业.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        self.df = df

    def total_unemployment_rate(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:, ['城镇调查失业率:全国']]
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        st.line_chart(pro_df.dropna().astype(float))

    def age_unemployment_rate(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :].copy()
        pro_df.columns = [i.replace(':', '-').replace("(停止)", "") for i in pro_df.columns]
        pro_df = pro_df.loc[:, ['全国16-24岁人口城镇调查失业率', '全国25-59岁人口城镇调查失业率']]
        st.line_chart(pro_df.dropna().astype(float))

    def eductaion_unemployment_rate(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :].copy()
        pro_df.columns = [i.replace(':', '-').replace("(停止)", "") for i in pro_df.columns]
        print(pro_df.columns)
        pro_df = pro_df.loc[:, ['全国25-59岁劳动力失业率-初中及以下学历', '全国25-59岁劳动力失业率-高中学历',
                                '全国25-59岁劳动力失业率-大专学历', '全国25-59岁劳动力失业率-本科及以上学历']]
        st.line_chart(pro_df.dropna().astype(float))

    def birth_death_rate(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:, ['人口出生率', '人口死亡率', '人口自然增长率']]
        st.line_chart(pro_df.dropna().astype(float))

    def increment_population(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:, ['总人口:城镇:增减', '总人口:乡村:增减']]
        st.line_chart(pro_df.dropna().astype(float))

    def graduation_population(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:, ['全国:高等学校毕业生数:本科']]
        pro_df.columns = [i.replace(':', '-') for i in pro_df]
        st.line_chart(pro_df.dropna().astype(float))


class Forex:
    def __init__(self):
        df = preprocess_choice_data('data/外汇.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        self.df = df

    def total_forex(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:, ['货币当局:国外资产:外汇', '货币当局:对其他存款性公司债权', '货币当局:储备货币']]
        pro_df['外汇债权合计'] = pro_df["货币当局:国外资产:外汇"] + pro_df["货币当局:对其他存款性公司债权"]
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        st.line_chart(pro_df.dropna().astype(float))

    def total_bank_exchange(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:, ['银行结售汇:差额:自身:当月值', '银行结售汇:差额:代客:当月值', '银行结售汇顺差:当月值']]
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        st.line_chart(pro_df.dropna().astype(float))

    def bank_spot_forex(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['银行远期结售汇:差额:当月值', '平均汇率:美元兑人民币']].reset_index()
        pro_df['平均汇率:美元兑人民币（逆序）'] = pro_df['平均汇率:美元兑人民币'].pct_change(1) * 100 * (-1)
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        bars = alt.Chart(pro_df).mark_bar().encode(
            x='指标名称',
            y='银行远期结售汇-差额-当月值'
        )
        line = alt.Chart(pro_df).mark_line(color='red').encode(
            x='指标名称',
            y='平均汇率-美元兑人民币（逆序）'
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(bars, line).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)

    def capital_current_account(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df['经常账户差额'] = pro_df['经常账户:差额:当季值']
        pro_df['资本金融账户差额'] = pro_df['资本和金融账户:差额:当季值'] - pro_df['金融账户:储备资产:储备资产:当季值']
        pro_df = pro_df.loc[:, ['经常账户差额', '资本金融账户差额']]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def balance_of_payments(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:,
                 ['经常账户:差额:当季值', '资本和金融账户:差额:当季值', '金融账户:储备资产:储备资产:当季值',
                  '净误差与遗漏:差额:当季值', '平均汇率:美元兑人民币']].reset_index()
        pro_df['经常账户差额'] = pro_df['经常账户:差额:当季值']
        pro_df['资本金融账户差额'] = pro_df['资本和金融账户:差额:当季值'] - pro_df['金融账户:储备资产:储备资产:当季值']
        pro_df['国际收支差额'] = pro_df['经常账户差额'] + pro_df['资本金融账户差额']
        pro_df['平均汇率:美元兑人民币（逆序）'] = pro_df['平均汇率:美元兑人民币'].pct_change(1) * 100 * (-1)
        pro_df = pro_df.loc[:, ['指标名称', '国际收支差额', '平均汇率:美元兑人民币（逆序）']].dropna()
        print(pro_df)
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        bars = alt.Chart(pro_df).mark_bar().encode(
            x='指标名称',
            y='国际收支差额'
        )
        line = alt.Chart(pro_df).mark_line(color='red').encode(
            x='指标名称',
            y='平均汇率-美元兑人民币（逆序）'
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(bars, line).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)

    def detail_current_account(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:,
                 ['经常账户:二次收入:差额:当季值', '经常账户:初次收入:差额:当季值', '经常账户:货物:差额:当季值',
                  '经常账户:服务:差额:当季值']]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def detail_capital_account(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:,
                 ['金融账户:非储备性质的金融账户:证券投资:当季值', '金融账户:非储备性质的金融账户:直接投资:当季值',
                  '金融账户:非储备性质的金融账户:其他投资:当季值']]
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)


class RealEstateInvest:
    def __init__(self):
        df = preprocess_choice_data('data/房地产投资.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        self.df = df

    def total_plot(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='real_estate_total_plot')
        pro_df = self.df.copy()
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[start_date:, ['房地产开发投资完成额:累计值', '房地产开发投资完成额:累计同比']].reset_index()
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        bars = alt.Chart(pro_df).mark_bar().encode(
            x='指标名称',
            y='房地产开发投资完成额-累计值'
        )
        line = alt.Chart(pro_df).mark_line(color='red').encode(
            x='指标名称',
            y='房地产开发投资完成额-累计同比'
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(bars, line).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)

    def season_plot(self):
        start_date = '2019-01'
        pro_df = self.df.loc[start_date:, ['房地产开发投资完成额:累计同比']]
        pro_df['月份'] = [i[-2:] for i in pro_df.index]
        pro_df['年份'] = [i[:4] for i in pro_df.index]
        pro_df = pro_df.pivot(index=['月份'], columns=['年份'], values='房地产开发投资完成额:累计同比')
        st.line_chart(pro_df)

    def construction_type(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='construction_type')
        pro_df = self.df.copy()
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[start_date:, ['房地产开发投资完成额:住宅:累计值', '房地产开发投资完成额:办公楼:累计值',
                                          '房地产开发投资完成额:商业营业用房:累计值',
                                          '房地产开发投资完成额:其他:累计值']]
        pro_df['房地产开发投资完成额:其他:累计值'] = pro_df['房地产开发投资完成额:其他:累计值'] / 1e4
        pro_df = pro_df.div(pro_df.sum(axis=1).replace(0, np.nan), axis=0)
        pro_df.columns = ['住宅', '办公楼', '商业营业用房', '其他']
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def using_type(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='using_type')
        pro_df = self.df.copy()
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[start_date:,
                 ['房地产开发投资完成额:建筑工程:累计值', '房地产开发投资完成额:安装工程:累计值',
                  '房地产开发投资完成额:设备工器具购置:累计值', '房地产开发投资完成额:其他费用:累计值']]
        pro_df = pro_df.div(pro_df.sum(axis=1).replace(0, np.nan), axis=0)
        pro_df.columns = ['建筑工程', '安装工程', '设备工器具购置', '其他费用']
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def area_type(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='area_type')
        pro_df = self.df.copy()
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[start_date:,
                 ['房地产开发投资完成额:东部地区:累计值', '房地产开发投资完成额:中部地区:累计值',
                  '房地产开发投资完成额:西部地区:累计值']]
        pro_df = pro_df.div(pro_df.sum(axis=1).replace(0, np.nan), axis=0)
        pro_df.columns = ['东部地区', '中部地区', '西部地区']
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def money_plot(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='money_plot')
        pro_df = self.df.copy()
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[start_date:, ['房地产开发投资:本年实际到位资金:合计:累计值',
                                          '房地产开发投资:本年实际到位资金:合计:累计同比']].reset_index()
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        bars = alt.Chart(pro_df).mark_bar().encode(
            x='指标名称',
            y='房地产开发投资:本年实际到位资金:合计:累计值'.replace(':', '-')
        )
        line = alt.Chart(pro_df).mark_line(color='red').encode(
            x='指标名称',
            y='房地产开发投资:本年实际到位资金:合计:累计同比'.replace(':', '-')
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(bars, line).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)

    def money_structure(self):
        start_date = '2000-01'
        on = st.toggle("仅显示第12月（年末）", key='money_structure')
        pro_df = self.df.copy()
        if on:
            pro_df['月份'] = [i[-2:] for i in pro_df.index]
            pro_df = pro_df[pro_df['月份'] == '12']
        pro_df = pro_df.loc[start_date:,
                 ['房地产开发企业到位资金:国内贷款:累计值', '房地产开发企业到位资金:利用外资:累计值',
                  '房地产开发企业到位资金:自筹资金:累计值', '房地产开发企业到位资金:定金及预收款:累计值',
                  '房地产开发企业到位资金:个人按揭贷款:累计值']]
        pro_df = pro_df.div(pro_df.sum(axis=1).replace(0, np.nan), axis=0)
        pro_df.columns = ['国内贷款', '利用外资', '自筹资金', '定金及预收款', '个人按揭贷款']
        pro_df = pro_df.astype(float)
        st.bar_chart(pro_df)

    def area_change(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, :]
        pro_df = pro_df.loc[:, ['房屋施工面积:累计值', '房屋新开工面积:累计值',
                                '房屋竣工面积:累计值', '商品房销售面积:累计值',
                                '商品房待售面积：累计值']]
        pro_df['净停工面积'] = pro_df['房屋新开工面积:累计值'] + (
                pro_df['房屋施工面积:累计值'] - pro_df['房屋竣工面积:累计值']).shift(1) - pro_df[
                                   '房屋施工面积:累计值']
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        st.line_chart(pro_df.dropna().astype(float))


def GDP_analysis():
    gdp = GDP()
    st.title('GDP总体分析')
    st.write('单位：百分比@月')
    gdp.total_plot()
    st.title('产业占比分析')
    st.write('单位：百分比@月')
    gdp.produce_proportion()
    st.title('产业增速分析')
    st.write('单位：百分比@月')
    gdp.produce_change()
    st.title('产业贡献分析')
    st.write('单位：百分比@月')
    gdp.produce_contribute()
    st.title('产业拉动分析')
    st.write('单位：百分比@月')
    gdp.produce_stimulation()
    st.title('支出占比分析')
    st.write('单位：百分比@月')
    gdp.revenue_proportion()
    st.title('支出贡献分析')
    st.write('单位：百分比@月')
    gdp.revenue_contribute()


def PMI_analysis():
    pmi = PMI()
    st.title('PMI总体分析')
    st.write('单位：特殊单位@月')
    pmi.total_plot()
    st.title('PMI需求分析')
    st.write('单位：特殊单位@月')
    pmi.demand_plot()
    st.title('PMI生产分析')
    st.write('单位：特殊单位@月')
    pmi.produce_plot()
    st.title('PMI采购分析')
    st.write('单位：特殊单位@月')
    pmi.procurement_plot()
    st.title('PMI库存分析')
    st.write('单位：特殊单位@月')
    pmi.inventory_plot()
    st.title('PMI价格分析')
    st.write('单位：特殊单位@月')
    pmi.price_plot()


def CPI_PPI_analysis():
    cpi_ppi = CPI_PPI()
    st.title('CPI+PPI总体分析')
    st.write('单位：百分比@月')
    cpi_ppi.total_plot()
    st.title('CPI分项分析')
    st.write('单位：百分比@月')
    cpi_ppi.cpi_plot()
    st.title('PPI分项分析')
    st.write('单位：百分比@月')
    cpi_ppi.ppi_plot()


def TRSCG_analysis():
    trscg = TRSCG()
    st.title('社零总体分析')
    st.write('单位：亿元/百分比@月')
    trscg.total_plot()
    st.title('社零分年份月度变化')
    st.write('单位：亿元@月')
    trscg.season_plot()
    st.title('汽车非汽车消费金额')
    st.write('单位：亿元@月')
    trscg.automobile_proportion()
    st.title('汽车非汽车消费增速')
    st.write('单位：百分比@月')
    trscg.automobile_increase()
    st.title('餐饮非餐饮消费金额')
    st.write('单位：亿元@月')
    trscg.goods_food_proportion()
    st.title('餐饮非餐饮消费增速')
    st.write('单位：百分比@月')
    trscg.goods_food_increase()
    st.title('城镇农村消费金额')
    st.write('单位：亿元@月')
    trscg.area_proportion()
    st.title('城镇农村消费增速')
    st.write('单位：百分比@月')
    trscg.area_increase()
    st.title('网上网下消费金额')
    st.write('单位：亿元@月')
    trscg.online_proportion()
    st.title('网上网下消费增速')
    st.write('单位：百分比@月')
    trscg.online_increase()
    st.title('限额非限额消费金额')
    st.write('单位：亿元@月')
    trscg.limit_proportion()
    st.title('限额非限额消费增速')
    st.write('单位：百分比@月')
    trscg.limit_increase()


def Export_analysis():
    export_basic = ExportBasic()
    st.title('进出口分币种计价增速情况')
    st.write('单位：百分比@月，包含人民币和美元计价两类增速')
    export_basic.total_plot()
    st.title('进出口绝对金额变化')
    st.write('单位：千美元@月')
    export_basic.amount_plot()
    st.title('出口总额增速分年份月度变化')
    st.write('单位：百分比@月')
    export_basic.output_season_plot()
    st.title('进口总额增速分年份月度变化')
    st.write('单位：百分比@月')
    export_basic.input_season_plot()

    export_country = ExportCountry()
    st.title('出口区域金额占比')
    st.write('单位：千美元，支持用户选择指定的月份')
    export_country.output_portion()
    st.title('进口区域金额占比')
    st.write('单位：千美元，支持用户选择指定的月份')
    export_country.input_portion()
    st.title('出口区域金额占比变化')
    st.write('单位：百分比@年，当前仅展示当前年份最大的5个区域的自2000年开始的历史占比变化')
    export_country.output_trend()
    st.title('进口区域金额占比变化')
    st.write('单位：百分比@年，当前仅展示当前年份最大的5个区域的自2000年开始的历史占比变化')
    export_country.input_trend()


def FixedAssetInvest_analysis():
    fixed_asset = FixedAssetInvest()
    st.title('固定资产投资总体走势')
    st.write('单位：亿元/百分比@月')
    fixed_asset.total_plot()
    st.title('固定资产投资分年份月度变化')
    st.write('单位：百分比@月')
    fixed_asset.season_plot()
    st.title('固定资产投资分建设性质变化')
    st.write('单位：百分比@月')
    fixed_asset.construct_type()
    st.title('固定资产投资分构成变化')
    st.write('单位：百分比@月')
    fixed_asset.portion()
    st.title('固定资产投资分产业变化')
    st.write('单位：百分比@月')
    fixed_asset.industry()
    st.title('固定资产投资分民间国企变化')
    st.write('单位：百分比@月')
    fixed_asset.state_owned()


def FinancingMoney_analysis():
    financing_money = FinancingMoney()
    st.title('社融总体走势')
    st.write('单位：亿元/百分比@月')
    financing_money.financing_plot()
    st.title('社融总体分年份月度变化')
    st.write('单位：亿元@月')
    financing_money.season_plot()
    st.title('社融总体结构构成')
    st.write('单位：亿元@月')
    financing_money.financing_portion()
    st.title('新增人民币贷款')
    st.write('单位：亿元@月')
    financing_money.increment_loan()
    st.title('表外资产变化')
    st.write('单位：亿元@月')
    financing_money.off_sheet()
    st.title('企业直接融资')
    st.write('单位：亿元@月')
    financing_money.direct_financing()
    st.title('社融其它组成')
    st.write('单位：亿元@月')
    financing_money.financing_other()
    st.title('货币供应量变化')
    st.write('单位：百分比@月')
    financing_money.money_plot()
    st.title('货币和社融增速剪刀差')
    st.write('单位：百分比@月')
    financing_money.money_scissors()


def Fiscal_analysis():
    fiscal = Fiscal()
    st.title('中央地方预算收入')
    st.write('单位：亿元@月')
    fiscal.central_budget_revenue()
    st.title('税收非税预算收入')
    st.write('单位：亿元@月')
    fiscal.tax_budget_revenue()
    st.title('税收分项收入')
    st.write('单位：亿元@月')
    fiscal.tax_detail_revenue()
    st.title('中央地方预算支出')
    st.write('单位：亿元@月')
    fiscal.central_budget_expenditure()
    st.title('预算支出分项')
    st.write('单位：亿元@月')
    fiscal.total_detail_expenditure()
    st.title('预算赤字情况')
    st.write('单位：亿元@月')
    fiscal.budget_deficit()
    st.title('中央地方政府基金收入')
    st.write('单位：亿元@月')
    fiscal.government_fund()
    st.title('土地出让金收入')
    st.write('单位：亿元@月')
    fiscal.land_grand_fee()


def PopulationEnployment_analysis():
    population_enployment = PopulationEnployment()
    st.title('总体失业率曲线')
    st.write('单位：百分比@月')
    population_enployment.total_unemployment_rate()
    st.title('不同年龄失业率情况')
    st.write('单位：百分比@月')
    population_enployment.age_unemployment_rate()
    st.title('不同学历失业率情况')
    st.write('单位：百分比@月')
    population_enployment.eductaion_unemployment_rate()
    st.title('出生率和死亡率')
    st.write('单位：百分比@年')
    population_enployment.birth_death_rate()
    st.title('新增城镇人口数量')
    st.write('单位：万人@年')
    population_enployment.increment_population()
    st.title('高校毕业生人数')
    st.write('单位：万人@年')
    population_enployment.graduation_population()


def Forex_analysis():
    forex = Forex()
    st.title('外汇和基础货币总体情况')
    st.write('单位：亿元@月')
    forex.total_forex()
    st.title('银行结售汇总体情况')
    st.write('单位：亿美元@月')
    forex.total_bank_exchange()
    st.title('结售汇远期结售汇和汇率')
    st.write('单位：亿美元/百分比@月')
    forex.bank_spot_forex()
    st.title('经常账户和资本账户')
    st.write('单位：亿美元@季')
    forex.capital_current_account()
    st.title('国际收支差额和汇率')
    st.write('单位：亿美元/百分比@季')
    forex.balance_of_payments()
    st.title('经常账户分项')
    st.write('单位：亿美元@季')
    forex.detail_current_account()
    st.title('金融账户分项')
    st.write('单位：亿美元@季')
    forex.detail_capital_account()


def RealEstateInvest_analysis():
    real_estate_invest = RealEstateInvest()
    st.title('房地产投资总体指数')
    st.write('单位：亿元/百分比@月')
    real_estate_invest.total_plot()
    st.title('房地产投资分年份月度变化')
    st.write('单位：百分比@月')
    real_estate_invest.season_plot()
    st.title('房地产投资分建筑类型')
    st.write('单位：百分比@月')
    real_estate_invest.construction_type()
    st.title('房地产投资分用途类型')
    st.write('单位：百分比@月')
    real_estate_invest.using_type()
    st.title('房地产投资分地区类型')
    st.write('单位：百分比@月')
    real_estate_invest.area_type()
    st.title('房地产投资到位资金')
    st.write('单位：亿元/百分比@月')
    real_estate_invest.money_plot()
    st.title('房地产投资资金结构分析')
    st.write('单位：百分比@月')
    real_estate_invest.money_structure()


if __name__ == "__main__":
    st.sidebar.markdown("# 中国宏观经济看板")
    st.sidebar.markdown("作者：AFAN（微信：afan-life）")
    st.sidebar.markdown("项目介绍：[macropage](https://github.com/AFAN-LIFE/macropage)")
    selection = st.sidebar.radio("当前支持的分析图表：",
                                 ["股票市场", "GDP分析", "社会消费品零售总额分析", "进出口分析", "固定资产投资分析", "CPI和PPI分析",
                                  "PMI分析", "社融和货币供应分析", "财政数据分析", "人口就业分析", "外汇分析",
                                  "房地产投资分析"
                                     # , "开发测试"
                                  ])
    if selection == "股票市场":
        from stock import stock_market_analysis
        stock_market_analysis()
    elif selection == "GDP分析":
        GDP_analysis()
    elif selection == "社会消费品零售总额分析":
        TRSCG_analysis()
    elif selection == "进出口分析":
        Export_analysis()
    elif selection == "固定资产投资分析":
        FixedAssetInvest_analysis()
    elif selection == "CPI和PPI分析":
        CPI_PPI_analysis()
    elif selection == "PMI分析":
        PMI_analysis()
    elif selection == "社融和货币供应分析":
        FinancingMoney_analysis()
    elif selection == "财政数据分析":
        Fiscal_analysis()
    elif selection == "人口就业分析":
        PopulationEnployment_analysis()
    elif selection == "外汇分析":
        Forex_analysis()
    elif selection == "房地产投资分析":
        RealEstateInvest_analysis()
    # elif selection == "开发测试":
    #     from test import test_func
    #     test_func()
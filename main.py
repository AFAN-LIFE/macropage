import re
import datetime
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from config import usernames
import streamlit_authenticator as stauth

# 如果数据有缺失值会因为数据类型不同而无法画图，所以这里有的用了大于2019-01来确保全部有数据
# 数据的列名不要有太多的:，不然会报错： If you are trying to use a column name that contains a colon, prefix it with a backslash; for example "column\:name" instead of "column:name".

class GDP:
    def __init__(self):
        df = pd.read_excel('data/GDP.xlsx')
        df = df[(df['指标名称'] >= '1992-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        df['月份'] = [i[-2:] for i in df.index]
        df['年份'] = [i[:4] for i in df.index]
        self.df = df

    def total_plot(self):
        pro_df = self.df.loc[:, ['中国:GDP:不变价:累计同比']]
        pro_df.columns = [i.replace('中国:', '').replace(':', '-') for i in pro_df.columns]
        st.write(pro_df)
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
        df = pd.read_excel('data/PMI.xlsx')
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
        df = pd.read_excel('data/CPI+PPI.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        self.df = df

    def total_plot(self):
        pro_df = self.df.loc[:, ['CPI:环比', 'PPI:全部工业品:环比']]
        start_date = '2019-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df)

    def cpi_plot(self):
        pro_df = self.df.loc[:, ['CPI:环比', 'CPI:食品:环比', 'CPI:非食品:环比']]
        start_date = '2019-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df)

    def ppi_plot(self):
        pro_df = self.df.loc[:, ['PPI:全部工业品:环比', 'PPI:生产资料:环比', 'PPI:生活资料:环比']]
        start_date = '2019-01'
        pro_df = pro_df.loc[start_date:, :]
        st.line_chart(pro_df)


class TRSCG:
    def __init__(self):
        df = pd.read_excel('data/社零.xlsx')
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
        start_date = '2019-01'
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
        pro_df = pro_df.pivot(index=['年份'], columns=['月份'], values='社会消费品零售总额:当月值')
        st.line_chart(pro_df)

    def automobile_proportion(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:,
                 ['社会消费品零售总额:当月值', '社会消费品零售总额:除汽车以外的消费品零售额:当月值']]
        pro_df.columns = ['总额', '除汽车']
        pro_df = pro_df.div(pro_df['总额'], axis=0)
        pro_df['汽车'] = pro_df['总额'] - pro_df['除汽车']
        st.bar_chart(pro_df.iloc[:, 1:])

    def automobile_increase(self):
        start_date = '2019-01'
        pro_df = self.df.loc[:, ['社会消费品零售总额:当月值', '社会消费品零售总额:除汽车以外的消费品零售额:当月值']]
        pro_df.columns = ['总额', '除汽车']
        pro_df['汽车'] = pro_df['总额'] - pro_df['除汽车']
        pro_df = pro_df.pct_change(10).loc[start_date:]
        st.line_chart(pro_df)

    def goods_food_proportion(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['社会消费品零售总额:商品零售:当月值', '社会消费品零售总额:餐饮收入:当月值']]
        pro_df.columns = ['商品零售', '餐饮收入']
        pro_df = pro_df.div(pro_df.sum(axis=1), axis=0)
        st.bar_chart(pro_df)

    def goods_food_increase(self):
        start_date = '2019-01'
        pro_df = self.df.loc[start_date:, ['社会消费品零售总额:当月值%', '社会消费品零售总额:商品零售:当月值%',
                                           '社会消费品零售总额:餐饮收入:当月值%']]
        pro_df.columns = ['总额', '商品零售', '餐饮收入']
        st.line_chart(pro_df)

    def area_proportion(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['社会消费品零售总额:城镇:当月值', '社会消费品零售总额:农村:当月值']]
        pro_df.columns = ['城镇', '农村']
        pro_df = pro_df.div(pro_df.sum(axis=1).replace(0, np.nan), axis=0)
        st.bar_chart(pro_df)

    def area_increase(self):
        start_date = '2019-01'
        pro_df = self.df.loc[start_date:,
                 ['社会消费品零售总额:当月值%', '社会消费品零售总额:城镇:当月值%', '社会消费品零售总额:农村:当月值%']]
        pro_df.columns = ['总额', '城镇', '农村']
        st.line_chart(pro_df)

    def online_proportion(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['社会消费品零售总额:当月值', '社会消费品零售总额:网上零售:当月值']]
        pro_df.columns = ['总额', '网上零售']
        pro_df = pro_df.div(pro_df['总额'].replace(0, np.nan), axis=0)
        pro_df['网下零售'] = pro_df['总额'] - pro_df['网上零售']
        st.bar_chart(pro_df.iloc[:, 1:])

    def online_increase(self):
        start_date = '2019-01'
        pro_df = self.df.loc[:, ['社会消费品零售总额:当月值', '社会消费品零售总额:网上零售:当月值']]
        pro_df.columns = ['总额', '网上零售']
        pro_df['网下零售'] = pro_df['总额'] - pro_df['网上零售']
        pro_df = pro_df.pct_change(10).loc[start_date:]
        st.line_chart(pro_df)

    def limit_proportion(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['社会消费品零售总额:当月值', '限额以上企业消费品零售总额:当月值']]
        pro_df.columns = ['总额', '限额']
        pro_df = pro_df.div(pro_df['总额'].replace(0, np.nan), axis=0)
        pro_df['非限额'] = pro_df['总额'] - pro_df['限额']
        st.bar_chart(pro_df.iloc[:, 1:])

    def limit_increase(self):
        start_date = '2019-01'
        pro_df = self.df.loc[:, ['社会消费品零售总额:当月值', '限额以上企业消费品零售总额:当月值']]
        pro_df.columns = ['总额', '限额']
        pro_df['非限额'] = pro_df['总额'] - pro_df['限额']
        pro_df = pro_df.pct_change(10).loc[start_date:]
        st.line_chart(pro_df)


class ExportBasic:
    def __init__(self):
        df = pd.read_excel('data/进出口基本.xlsx')
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
        pro_df['进出口金额:当月值'] = pro_df['进出口金额:当月值'] / 1e5  # 单位统一
        st.line_chart(pro_df)


class FixedAsset:
    def __init__(self):
        df = pd.read_excel('data/固定资产.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        self.df = df

    def total_plot(self):
        start_date = '2013-01'
        pro_df = self.df.loc[start_date:, ['固定资产投资完成额:累计值', '固定资产投资完成额:累计同比']].reset_index()
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

    def construct_type(self):
        start_date = '2019-01'
        pro_df = self.df.loc[start_date:, ['固定资产投资完成额:新建:累计同比', '固定资产投资完成额:扩建:累计同比',
                                           '固定资产投资完成额:改建:累计同比']]
        pro_df.columns = ['新建', '扩建', '改建']
        pro_df = pro_df.astype(float)
        st.line_chart(pro_df)


def GDP_analysis():
    st.title('GDP分析')
    gdp = GDP()
    gdp.total_plot()
    gdp.produce_proportion()
    gdp.produce_change()
    gdp.produce_contribute()
    gdp.produce_stimulation()
    gdp.revenue_proportion()
    gdp.revenue_contribute()


def PMI_analysis():
    pmi = PMI()
    pmi.total_plot()
    pmi.demand_plot()
    pmi.produce_plot()
    pmi.procurement_plot()
    pmi.inventory_plot()
    pmi.price_plot()


def CPI_PPI_analysis():
    cpi_ppi = CPI_PPI()
    cpi_ppi.total_plot()
    cpi_ppi.cpi_plot()
    cpi_ppi.ppi_plot()


def TRSCG_analysis():
    st.title('社会消费品零售总额分析')
    trscg = TRSCG()
    trscg.total_plot()
    trscg.season_plot()
    trscg.automobile_proportion()
    trscg.automobile_increase()
    trscg.goods_food_proportion()
    trscg.goods_food_increase()
    trscg.area_proportion()
    trscg.area_increase()
    trscg.online_proportion()
    trscg.online_increase()
    trscg.limit_proportion()
    trscg.limit_increase()


def ExportBasic_analysis():
    st.title('进出口分析')
    export_basic = ExportBasic()
    export_basic.total_plot()
    export_basic.amount_plot()


def FixedAsset_analysis():
    fixed_asset = FixedAsset()
    fixed_asset.total_plot()
    fixed_asset.construct_type()

authenticator = stauth.Authenticate(
    credentials={'usernames': usernames},
    cookie_name='some_cookie_name', key='some_signature_key', cookie_expiry_days=30)
authenticator.login('Login', 'main')
print(st.session_state.__dict__)

if st.session_state["authentication_status"] and st.session_state["username"]=="admin":
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.sidebar.markdown("# 中国宏观经济看板")
    selection = st.sidebar.radio("作者：AFAN的金融科技", ["GDP分析", "社会消费品零售总额分析", "进出口分析", "固定资产投资分析", "CPI和PPI分析", "PMI分析"])
    if selection=="GDP分析":
        GDP_analysis()
    elif selection=="社会消费品零售总额分析":
        TRSCG_analysis()
    elif selection=="进出口分析":
        ExportBasic_analysis()
    elif selection=="固定资产投资分析":
        FixedAsset_analysis()
    elif selection=="CPI和PPI分析":
        CPI_PPI_analysis()
    elif selection=="PMI分析":
        PMI_analysis()

elif st.session_state["authentication_status"] and st.session_state["username"]=="guest":
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.write('当前用户身份为访客用户，请联系管理员解锁更多功能')
    GDP_analysis()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
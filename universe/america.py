import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
from tool import preprocess_choice_data


class AmericaBasic:
    def __init__(self):
        df = preprocess_choice_data('data/美国宏观.xlsx')
        df = df[(df['指标名称'] >= '2000-01') & (df['指标名称'] <= '2099-01')]
        df = df.replace('--', np.nan)
        df = df.set_index('指标名称').sort_index()
        self.df = df

    def employment_number_plot(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['美国:非农就业人数:季调', '美国:新增非农就业人数:当月值:季调']]
        c1, c2 = st.columns([1, 1])
        selected_start_date = c1.selectbox('开始日期', options=pro_df.index.tolist(), index=len(pro_df) - 24,
                                           key='start_employment_number_plot')
        selected_end_date = c2.selectbox('结束日期', options=pro_df.index.tolist(), index=len(pro_df) - 1,
                                         key='end_employment_number_plot')
        pro_df = pro_df.loc[selected_start_date:selected_end_date, :].reset_index()
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        bars = alt.Chart(pro_df).mark_bar().encode(
            x='指标名称',
            y='美国:非农就业人数:季调'.replace(':', '-')
        )
        line = alt.Chart(pro_df).mark_line(color='red').encode(
            x='指标名称',
            y='美国:新增非农就业人数:当月值:季调'.replace(':', '-')
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(bars, line).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)

    def unemployment_ratio_plot(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['美国:失业率:季调', '美国:劳动参与率']]
        c1, c2 = st.columns([1, 1])
        selected_start_date = c1.selectbox('开始日期', options=pro_df.index.tolist(), index=len(pro_df) - 24,
                                           key='start_unemployment_ratio_plot')
        selected_end_date = c2.selectbox('结束日期', options=pro_df.index.tolist(), index=len(pro_df) - 1,
                                         key='end_unemployment_ratio_plot')
        pro_df = pro_df.loc[selected_start_date:selected_end_date, :].reset_index()
        # 指定开始结束时间，否则会从0开始展示，效果不好
        join_min, join_max = int(pro_df['美国:劳动参与率'].min()), int(pro_df['美国:劳动参与率'].max() + 1)
        pro_df.columns = [i.replace(':', '-') for i in pro_df.columns]
        ind1, ind2 = '美国:失业率:季调'.replace(':', '-'), '美国:劳动参与率'.replace(':', '-')
        line1 = alt.Chart(pro_df).mark_line().encode(
            x='指标名称',
            y=ind1,
        )
        line2 = alt.Chart(pro_df).mark_line(color='red').encode(
            x='指标名称',
            y=alt.Y(ind2, scale=alt.Scale(domain=[join_min, join_max])),  # 这里替换起始值和结束值
        )
        # 将柱状图和折线图组合在一起
        chart = alt.layer(line1, line2).resolve_scale(y='independent')
        st.altair_chart(chart, use_container_width=True)

    def cpi_ppi_plot(self):
        pro_df = self.df.loc[:, ['美国:CPI:非季调:当月同比', '美国:PPI:产成品:当月同比']]
        start_date = '2000-01'
        pro_df = pro_df.loc[start_date:, :]
        c1, c2 = st.columns([1, 1])
        selected_start_date = c1.selectbox('开始日期', options=pro_df.index.tolist(), index=len(pro_df) - 24,
                                           key='start_cpi_ppi_plot')
        selected_end_date = c2.selectbox('结束日期', options=pro_df.index.tolist(), index=len(pro_df) - 1,
                                         key='end_cpi_ppi_plot')
        pro_df = pro_df.loc[selected_start_date:selected_end_date, :]
        st.line_chart(pro_df.astype(float))

    def pmi_plot(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['美国:供应管理协会(ISM):PMI:季调', '美国:供应管理协会(ISM):服务业PMI:季调']]
        c1, c2 = st.columns([1, 1])
        selected_start_date = c1.selectbox('开始日期', options=pro_df.index.tolist(), index=len(pro_df) - 24,
                                           key='start_pmi_plot')
        selected_end_date = c2.selectbox('结束日期', options=pro_df.index.tolist(), index=len(pro_df) - 1,
                                         key='end_pmi_plot')
        pro_df = pro_df.loc[selected_start_date:selected_end_date, :]
        st.line_chart(pro_df.astype(float))

    def m1_m2_ratio_plot(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:, ['美国:M1:季调:当月同比', '美国:M2:季调:当月同比']]
        c1, c2 = st.columns([1, 1])
        selected_start_date = c1.selectbox('开始日期', options=pro_df.index.tolist(), index=len(pro_df) - 24,
                                           key='start_m1_m2_ratio_plot')
        selected_end_date = c2.selectbox('结束日期', options=pro_df.index.tolist(), index=len(pro_df) - 1,
                                         key='end_m1_m2_ratio_plot')
        pro_df = pro_df.loc[selected_start_date:selected_end_date, :]
        st.line_chart(pro_df.astype(float))

    def export_plot(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:,
                 ['美国:出口金额:季调', '美国:进口金额:季调', '美国:贸易差额:季调']].astype(float)
        c1, c2 = st.columns([1, 1])
        selected_start_date = c1.selectbox('开始日期', options=pro_df.index.tolist(), index=len(pro_df) - 24,
                                           key='start_export_plot')
        selected_end_date = c2.selectbox('结束日期', options=pro_df.index.tolist(), index=len(pro_df) - 1,
                                         key='end_export_plot')
        pro_df = pro_df.loc[selected_start_date:selected_end_date, :]
        st.line_chart(pro_df)

    def fiscal_plot(self):
        start_date = '2000-01'
        pro_df = self.df.loc[start_date:,
                 ['美国:政府财政收入', '美国:政府财政支出', '美国:政府财政赤字(盈余为负)']].astype(float)
        c1, c2 = st.columns([1, 1])
        selected_start_date = c1.selectbox('开始日期', options=pro_df.index.tolist(), index=len(pro_df) - 24,
                                           key='start_fiscal_plot')
        selected_end_date = c2.selectbox('结束日期', options=pro_df.index.tolist(), index=len(pro_df) - 1,
                                         key='end_fiscal_plot')
        pro_df = pro_df.loc[selected_start_date:selected_end_date, :]
        st.line_chart(pro_df)


def AmericaBasic_analysis():
    america_basic = AmericaBasic()
    st.title('非农人口就业情况')
    st.write('单位：千人@月')
    america_basic.employment_number_plot()
    st.title('失业率和劳动参与率')
    st.write('单位：百分比@月')
    america_basic.unemployment_ratio_plot()
    st.title('CPI和PPI情况')
    st.write('单位：百分比@月')
    america_basic.cpi_ppi_plot()
    st.title('ISM PMI和情况')
    st.write('单位：百分比@月')
    america_basic.pmi_plot()
    st.title('M1和M2增速情况')
    st.write('单位：百分比@月')
    america_basic.m1_m2_ratio_plot()
    st.title('进出口情况')
    st.write('单位：百万美元@月')
    america_basic.export_plot()
    st.title('财政情况')
    st.write('单位：百万美元@月')
    america_basic.fiscal_plot()

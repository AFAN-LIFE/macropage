import time
import altair as alt
import pandas as pd
import streamlit as st


class BondInterest:
    def __init__(self):
        self.yield_df = pd.read_csv('data/yield.csv')
        # self.tf_continuous_df = pd.read_csv('data/tf_continuous.csv')

    def yield_curve(self):
        yield_df = self.yield_df.copy().set_index('workTime')
        term_dict = {
            'threeMonth': '3m',
            'sixMonth': '6m',
            'oneYear': '1y',
            'twoYear': '3y',
            'fiveYear': '5y',
            'sevenYear': '7y',
            'tenYear': '10y',
            'fifteenYear': '15y',
            'twentyYear': '20y',
            'thirtyYear': '30y'
        }
        yield_df = yield_df.rename(term_dict, axis=1)
        term_order = ['3m', '6m', '1y', '3y', '5y', '7y', '10y', '15y', '20y', '30y']
        yield_df = yield_df.loc[:, term_order]
        options = yield_df.index.tolist()
        options = sorted(options)
        date = st.select_slider("请选择想要查询的日期", options=options, key='yield_curve', value=options[-1])

        # 创建2个空的容器
        slider_container = st.empty()
        chart_container = st.empty()
        c1, c2, c3, c4 = st.columns([1,1,1,1])
        c1.markdown(f"<div style='padding-top: 35px; padding-bottom: 10px'>播放速度：日/秒</div>",
                      unsafe_allow_html=True)
        speed = c2.number_input('', value=100)
        c3.markdown(f"<div style='padding-top: 35px; padding-bottom: 10px'>播放起始时间</div>",
                      unsafe_allow_html=True)
        start_play = c4.selectbox('', options, index=len(options)-252)
        run = st.button("播放动画", key='output_run', type='primary')
        def run_plot(date, object):
            selected_df = yield_df.loc[date, :]
            data = pd.DataFrame({
                'Term': selected_df.index,
                'Yield': selected_df.values
            })
            chart = alt.Chart(data.dropna()).mark_line(point=True).encode(
                x=alt.X('Term:N', sort=term_order, title='Term'),
                y=alt.Y('Yield:Q', title='Yield (%)'),
                tooltip=['Term:N', 'Yield:Q']
            )
            object.altair_chart(chart, use_container_width=True)

        if run:
            start_idx = options.index(start_play)
            for i in options[start_idx:]:
                time.sleep(1/speed)
                slider_container.select_slider("Select Date", options=options, value=i, key=i)
                run_plot(i, chart_container)
        else:
            run_plot(date, st)

    def time_series_yield(self):
        yield_df = self.yield_df.copy().set_index('workTime')
        term_dict = {
            'threeMonth': '3m',
            'sixMonth': '6m',
            'oneYear': '1y',
            'twoYear': '3y',
            'fiveYear': '5y',
            'sevenYear': '7y',
            'tenYear': '10y',
            'fifteenYear': '15y',
            'twentyYear': '20y',
            'thirtyYear': '30y'
        }
        yield_df = yield_df.rename(term_dict, axis=1)
        term_order = ['3m', '6m', '1y', '3y', '5y', '7y', '10y', '15y', '20y', '30y']
        options = yield_df.index.tolist()
        options = sorted(options)
        show_term_list = st.multiselect('请选择要展示的时期（可多个）', options=term_order, default=term_order)
        c1, c2 = st.columns([1, 1])
        start_date = c1.selectbox('开始日期', options=options, index=len(options) - 30 * 2,
                                           key='start_term_date')
        end_date = c2.selectbox('结束日期', options=options, index=len(options) - 1,
                                         key='end_term_date')
        selected_df = yield_df.loc[str(start_date):str(end_date), show_term_list]
        st.line_chart(selected_df)
        st.write(selected_df)

    # def tf_continuous_plot(self):
    #     tf_continuous_df = self.tf_continuous_df.copy()
    #     tf_continuous_df['trade_date'] = tf_continuous_df['trade_date'].astype(str)
    #     pivot_df = tf_continuous_df.pivot(index='trade_date', columns='ts_code')
    #     code_dict = {
    #         'TS.CFX': '2y',
    #         'TF.CFX': '5y',
    #         'T.CFX': '10y',
    #         'TL.CFX': '30y',
    #     }
    #     pivot_df = pivot_df.rename(code_dict, axis=1)
    #     options = pivot_df.index.tolist()
    #     start_date, end_date = st.select_slider("请选择想要查询的日期", options=options, key='tf_continuous',
    #                                             value=(options[0], options[-1]))
    #     selected_df = pivot_df.loc[str(start_date):str(end_date), :]
    #     st.write(selected_df)
    #     st.line_chart(selected_df)


def bond_interest_analysis():
    bond_interest = BondInterest()
    st.title('国债收益率曲线（截面）')
    st.write('单位：百分比@日')
    bond_interest.yield_curve()
    st.title('国债收益率曲线（时序）')
    st.write('单位：百分比@日')
    bond_interest.time_series_yield()

    # st.title('国债期货走势图')
    # st.write('单位：元@日')
    # bond_interest.tf_continuous_plot()
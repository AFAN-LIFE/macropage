def test_func():
    import streamlit as st
    import time
    from datetime import datetime, timedelta

    # 创建10天的日期列表
    start_date = datetime.today()
    date_list = [start_date + timedelta(days=i) for i in range(10)]

    # 创建一个空的容器，用于放置 select_slider
    slider_container = st.empty()

    # 使用 select_slider 创建一个带有日期的滑块
    selected_date = slider_container.select_slider("Select Date", options=date_list,
                                                   format_func=lambda x: x.strftime('%Y-%m-%d'))

    # 创建一个按钮
    start_animation = st.button("Start Animation")

    # 如果按钮被点击，开始动画效果
    if start_animation:
        for date in date_list:
            # 在同一个滑块上更新日期
            slider_container.select_slider("Select Date", options=date_list, value=date,
                                           format_func=lambda x: x.strftime('%Y-%m-%d'), key=date)
            time.sleep(0.1)
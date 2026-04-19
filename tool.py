import pandas as pd
import streamlit as st

def preprocess_choice_data(path):
    df = pd.read_excel(path, skiprows=1)
    df = df.iloc[:, 1:]
    df.columns = [i.replace("：", ":") for i in df.columns]
    return df

@DeprecationWarning
# 前版本choice因为出口国家金额量纲不统一编写
def get_choice_unit_arr(path, expected_set):
    df = pd.read_excel(path, skiprows=1)
    unit_se = df.iloc[2, 1:]
    assert set(unit_se) == expected_set
    def trans(x):
        if x=='万美元':
            return 1
        elif x=='千美元':
            return 0.1
        else:
            raise Exception('不存在的单位')
    correct_arr = unit_se.apply(trans)
    return correct_arr

# 全局月份选择器相关函数
def init_global_month():
    """初始化全局月份状态"""
    if 'global_month' not in st.session_state:
        st.session_state.global_month = None
    if 'global_month_set' not in st.session_state:
        st.session_state.global_month_set = False

def get_global_month():
    """获取全局月份"""
    return st.session_state.get('global_month', None)

def set_global_month(month):
    """设置全局月份"""
    st.session_state.global_month = month
    st.session_state.global_month_set = True

def find_closest_date(options, target_date, is_end_date=False):
    """
    在日期列表中找到最接近目标日期的日期
    如果目标日期不存在，找到最近的可用日期
    """
    if not target_date or not options:
        return None
    
    # 将选项转换为日期对象进行比较
    def parse_date(date_str):
        try:
            return pd.to_datetime(date_str)
        except:
            return None
    
    options_dates = [parse_date(d) for d in options]
    target = parse_date(target_date)
    
    if target is None:
        return None
    
    # 过滤掉无效日期
    valid_pairs = [(d, idx) for idx, d in enumerate(options_dates) if d is not None]
    if not valid_pairs:
        return None
    
    # 找到最接近的日期
    if is_end_date:
        # 对于结束日期，找小于等于目标日期的最大日期
        candidates = [(d, idx) for d, idx in valid_pairs if d <= target]
        if candidates:
            return max(candidates, key=lambda x: x[0])[1]
        # 如果没有小于等于的，找最小的日期
        return min(valid_pairs, key=lambda x: x[0])[1]
    else:
        # 对于开始日期，找小于等于目标日期的最大日期（优先选择目标日期或更早的日期）
        candidates = [(d, idx) for d, idx in valid_pairs if d <= target]
        if candidates:
            return max(candidates, key=lambda x: x[0])[1]
        # 如果没有小于等于的，找最小的日期
        return min(valid_pairs, key=lambda x: x[0])[1]

def get_date_index(options, default_index, is_end_date=False):
    """
    获取日期选择器的索引
    如果设置了全局月份，使用全局月份；否则使用默认索引
    """
    global_month = get_global_month()
    if global_month and st.session_state.get('global_month_set', False):
        closest_idx = find_closest_date(options, global_month, is_end_date)
        if closest_idx is not None:
            return closest_idx
    return default_index
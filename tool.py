import pandas as pd

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
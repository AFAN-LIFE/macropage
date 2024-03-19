# 中国宏观经济看板
 
作者：AFAN  
来源：AFAN的金融科技

## 环境管理

`Python=3.9`，推荐另外新建conda环境，防止交叉污染：

```
conda create -n macropage python=3.9
```

Python的核心包版本：

```
streamlit                    1.29.0
streamlit-authenticator      0.2.3
matplotlib                   3.8.0
pandas                       2.1.1
cryptography                 41.0.4
openpyxl                     3.1.2
```

一步安装：

```
pip install pandas==2.1.1 openpyxl==3.1.2 matplotlib==3.8.0 streamlit==1.29.0 streamlit-authenticator==0.2.3 cryptography==41.0.4
```


## 项目启动

在macropage的conda环境下执行：

```
streamlit run main.py
```

默认在`http://localhost:8501/`启动


## 参考文档

- [Streamlit官网API操作手册](https://docs.streamlit.io/library/api-reference)

- [Hello Github介绍streamlit](https://github.com/HelloGitHub-Team/Article/blob/master/contents/Python/Streamlit/content.md)

- [Streamlit-Authenticator加密登录](https://github.com/mkhorasani/Streamlit-Authenticator)

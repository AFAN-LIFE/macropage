# China Macroeconomic Dashboard
**其他语言版本: [English](README.md), [中文](README_zh.md).**

**Author: AFAN (WeChat: afan-life, Email: fcncassandra@gmail.com)**  
**Online address: https://macropage.streamlit.app/**

**Citation Notice: This project is under the CC-BY license. Anyone can use the demo but must cite the source.**

**The following content is translated by ChatGPT**

## Data Information

Most of the data in this project is currently exported by myself using the Choice financial terminal. There may be plans to use other data interfaces or expand the data in the future, but unless something unexpected happens, the data will be **updated at least once a month**.

Due to the different update times of various macroeconomic data, there may sometimes be cases where the latest data is not fully updated. Please understand. For detailed data updates, please refer to the [2024 National Bureau of Statistics Data Release Calendar](https://www.stats.gov.cn/xxgk/sjfb/fbrcb/202312/t20231229_1946090.html).

The project's data is stored in the [data](data)folder, and the categories currently included are:

- 1 GDP data
- 2 Retail sales data
- 3 Basic import and export data, regional import and export data
- 4 Fixed asset investment data
- 5 CPI and PPI data
- 6 PMI data
- 7 Social financing and monetary data
- 8 Fiscal data
- 9 Population and employment data
- 10 Foreign exchange data
- 11 Real estate investment data
- 12 Basic stock market data, stock index data
- 13 Government bond yield curve data

## Environment Management

It is recommended to use `Python=3.9` for this project and create a separate conda environment to prevent version conflicts:

```
conda create -n macropage python=3.9
```

Core Python package versions:

```
streamlit                    1.29.0
streamlit-authenticator      0.2.3
matplotlib                   3.8.0
pandas                       2.1.1
cryptography                 41.0.4
openpyxl                     3.1.2
streamlit-echarts            0.4.0
altair                       5.2.0
tushare
```

Install in one step:

```
pip install pandas==2.1.1 openpyxl==3.1.2 matplotlib==3.8.0 streamlit==1.29.0 streamlit-authenticator==0.2.3 cryptography==41.0.4 tushare
```

## Project Launch

Run the following command in the macropage conda environment:

```
streamlit run main.py
```

The project will start at `http://localhost:8501/` by default.

## In-depth Project Learning

- Scan the code to join the Knowledge Planet: AFAN's Fintech, where you can watch past macroeconomic data analysis columns and Streamlit teaching sessions in the live stream playback:

<img src="asset/planet.jpg" title="" alt="Knowledge Planet: AFAN's Fintech" width="199">

- Contact AFAN on WeChat to join the Fintech Learning Community (WeChat: afan-life):  

<img src="asset/weixin.png" title="" alt="WeChat: afan-life" width="199">

## Project Background

Last year (2023), I accidentally bought a copy of Li Qilin's book "Macro Economic Data Analysis Handbook" and found it to be fascinating. My undergraduate and master's studies were in finance, so I naturally learned a lot of macroeconomic knowledge from textbooks. However, I had little understanding of how this data was collected, its standards, update frequency, and the relationships between different data categories.

Later, I started working in fintech and grew to prefer more direct things like code and models. This book gave me the same feeling. So I thought, why not use the Choice financial data platform to obtain all the macroeconomic data in this handbook and then implement it all in Python code?

Soon, I implemented most of the analysis charts in my Knowledge Planet: **[AFAN's Fintech](https://t.zsxq.com/QBfx5)**. Not long ago, I also taught **[Streamlit](https://t.zsxq.com/ip6Zt)**, a very useful Python open-source visualization framework, in my regular live streams. So I thought, why not combine the two into an open-source project?

This project follows the CC-BY license, meaning anyone can freely use and modify it, but you must cite the source. If you cannot deploy it locally, this project has also been published on the Streamlit community, and [you can access it directly](https://macropage.streamlit.app/). If you have further customization needs, feel free to contact me for paid cooperation.

With this open-source project, those interested in the economy can gain a more intuitive understanding of real data. Some content creators can also use this as a supplementary material for their videos, including myself. If you encounter any issues while using it, you can raise an issue or add me on WeChat: afan-life for discussion.

## Development References

- [Streamlit Official API Documentation](https://docs.streamlit.io/library/api-reference)

- [Streamlit-Authenticator for Secure Login](https://github.com/mkhorasani/Streamlit-Authenticator)

- [Altair Charts](https://altair.streamlit.app/)

## Project-Based Creations
- [August 2024 Review: Can the September Market Momentum Continue? Focus on Fiscal Policy, Real Estate, and Exports](https://www.bilibili.com/video/BV19r11YrES6/)
- [July 2024 Review: Continuous Growth in Fixed Investment, Credit Expansion Contrasts with Declining Social Financing](https://www.bilibili.com/video/BV1roWWexEmC/)
- [Central Bank Intervenes! Animated Treasury Yield Curve](https://www.bilibili.com/video/BV1jx4y187ws/)  
- [Strong Exports, Weak Imports, ASEAN's Share Keeps Growing](https://www.bilibili.com/video/BV14M4m1U7iK/)  
- [Building a China Macroeconomic Data Dashboard with Streamlit](https://www.bilibili.com/video/BV1fJ4m1u7u9/)


## Update Log
- 2024/10/07:
  - Data Update: Updated macroeconomic data
  - Feature Update: Added the housing price index for 70 cities and the unemployment rate excluding students

- 2024/08/09:
  - Data Update: Updated macroeconomic data
  - Feature Update: Added GitHub Actions for daily updates of Tushare and yield curve data

- 2024/07/01:
  - Data Update: Updated stock market data
  - Feature Update: Added bond yield curve data from the Ministry of Finance

- 2024/06/21:
  - Data Update: Updated May macroeconomic data

- 2024/06/20:
  - Data Update:
    - Due to a Choice software issue, May macroeconomic data has not been updated
    - Updated the latest stock-related data from Tushare
  - Feature Update: Added stock market analysis module

- 2024/06/09:
  - Data Update: Updated basic import and export.xlsx and import and export countries.xlsx
  - Feature Update: Added a button to play pie chart animations in the import and export analysis section
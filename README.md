# 中国宏观经济看板
**其他语言版本: [English](README.md), [中文](README.md).**

**作者：AFAN（微信：afan-life，邮箱：fcncassandra@gmail.com)**
**在线地址：https://macropage.streamlit.app/**

[![Macropage主页](asset/homepage.png)](https://macropage.streamlit.app/)

**引用说明：本项目为CC-BY协议，任何人都可以使用演示，但需要注明出处**

## 数据说明

本项目的数据目前大部分都是我自己用choice金融终端导出来的，未来也可能有计划使用其他的数据接口或者扩充更多的数据，但是不出意外至少会**1个月刷新1次数据**。

由于不同宏观经济数据的更新时间不统一，所以有时候可能出现最新数据中未更新完的情况，请谅解。详细的数据更新请查看[2024年统计局数据日历](https://www.stats.gov.cn/xxgk/sjfb/fbrcb/202312/t20231229_1946090.html)

项目的数据都在[data](data)文件夹下，当前已经包含的数据类别有：

- 1 GDP数据
- 2 社零数据
- 3 进出口基本数据、进出口区域数据
- 4 固定资产投资数据
- 5 CPI和PPI数据
- 6 PMI数据
- 7 社融和货币数据
- 8 财政数据
- 9 人口就业数据
- 10 外汇数据
- 11 房地产投资数据
- 12 股票基本数据、股票指数数据
- 13 国债收益率曲线数据
- 14 美国宏观经济数据

## 环境管理

本工程推荐使用`Python=3.9`，并建议另外新建conda环境，防止版本交叉污染：

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
streamlit-echarts            0.4.0
altair                       5.2.0
tushare
```

一步安装：

```
pip install pandas==2.1.1 openpyxl==3.1.2 matplotlib==3.8.0 streamlit==1.29.0 streamlit-authenticator==0.2.3 cryptography==41.0.4 tushare
```

## 项目启动

在macropage的conda环境下执行：

```
streamlit run main.py
```

默认在`http://localhost:8501/`启动

## docker部署使用

### 镜像获取

网络条件允许可以直接docker下拉镜像：

```shell
docker pull afanlife/macropage:v1.1
```

网络条件受限，可以切换到本工程目录后，根据Dockerfile进行build：

```shell
docker build -t macropage:v1.1 .
```

### 容器启动

#### 方式1：基于compose启动（推荐）

基于本地已经编写好的compose.yaml直接启动

```shell
docker compose up -d  # 启动并创建所有容器
docker compose down  # 停止并清除所有容器
```


#### 方式2：手动启动容器

可以切换到本工程目录后，执行以下代码进行项目启动，启动成功即可在`http://localhost:8501/` 查看本地部署实例

```shell
docker run -d -p 8501:8501 -v .:/opt/code --name macropage-app macropage:v1.1 bash -c "cd /opt/code && streamlit run main.py"
```

#### 相关辅助指令

```shell
docker logs macropage-app  # 启动失败可以查看容器内部的运行日志
docker exec -it macropage-app /bin/bash  # 启动后可以进入容器后查看 
exit  # 容器内退出
```

## 深入学习项目

- 扫码加入知识星球：AFAN的金融科技，收看专栏中的宏观经济数据往期分析，以及直播回放中的streamlit教学：

<img src="asset/planet.jpg" title="" alt="知识星球：AFAN的金融科技" width="199">

- 微信联系AFAN，加入金融科技学习社群（微信：afan-life）：  

<img src="asset/weixin.png" title="" alt="微信：afan-life" width="199">


## 项目说明

去年（2023年）的时候，我偶然买到了一本李奇霖老师的《宏观经济数据分析手册》，翻阅一下就爱不释手。我的本硕都是金融类专业，自然是从课本中学到很多宏观经济知识，但是对于这些数据怎么采集的、口径是如何、更新频率是多少，以及不同类别数据中存在的关系，其实是知之甚少。

后来我一直从事金融科技的相关工作，也更喜欢代码和模型这些更直接的东西，这本书给我的感觉也是如此。于是我就想到何不把这里面的宏观经济数据手册的数据利用choice金融数据平台全部获取后，自己编写Python代码全部实现一遍？

很快我在自己的知识星球：**[AFAN的金融科技](https://t.zsxq.com/QBfx5)** 中，把这里面大部分的分析图表做了代码实现。此外不久前，我在自己的星球定期直播中 **[教学了streamlit](https://t.zsxq.com/ip6Zt)** 这个非常好用的Python开源可视化框架，就想着能不能结合到一起变成一个开源项目。

本项目遵循CC-BY协议，也即大家可以用完全自由的使用和修改这个项目，但是要注明来源。如果不会本地部署的话，这个项目在streamlit社区上也进行了发布，[可以直接访问](https://macropage.streamlit.app/)。如果有进一步的定制开发的需要，也可以找我付费合作~

利用这个开源项目，对经济感兴趣的小伙伴可以更加直观的了解到真实数据的情况，一些自媒体的UP主也可以利用这个作为视频中的素材补充，当然也包括我哈哈。欢迎大家使用中有问题也可以给我提issues或者加我微信：afan-life进行交流~


## 开发参考文档

- [Streamlit官网API操作手册](https://docs.streamlit.io/library/api-reference)

- [Streamlit-Authenticator加密登录](https://github.com/mkhorasani/Streamlit-Authenticator)

- [altair图表](https://altair.streamlit.app/)

- [echarts图表](https://echarts.streamlit.app/)

## 基于项目的创作
- [24年11月回顾：货币政策转向明显，国债利率跌破警线 ](https://www.bilibili.com/video/BV1CskBYbEaq/)
- [24年10月回顾：川普胜选比特币飞涨，地产企稳十万亿启动 ](https://www.bilibili.com/video/BV14DSwYnE9N/)
- [24年9月回顾：炒股炒坏剪刀差？外商投资下滑加快](https://www.bilibili.com/video/BV1YxCoYeEqJ/)
- [24年8月回顾：九月行情能否延续？关注财政政策和地产出口](https://www.bilibili.com/video/BV19r11YrES6/)
- [24年7月回顾：固定投资持续加码，信贷放水社融逆行](https://www.bilibili.com/video/BV1roWWexEmC/)
- [央行出手！动画国债收益率曲线](https://www.bilibili.com/video/BV1jx4y187ws/)  
- [出口强劲进口弱，东盟占比节节高](https://www.bilibili.com/video/BV14M4m1U7iK/)  
- [用Streamlit搭建中国宏观经济数据看板](https://www.bilibili.com/video/BV1fJ4m1u7u9/)

## 更新记录
- 2024/12/19：月度更新 

- 2024/11/19:
  - 数据更新：
    - 更新了宏观经济数据
    - 增加了部分美国股票指数数据

- 2024/10/19:
  - 数据更新：
    - 更新了宏观经济数据
    - 增加了部分美国宏观数据

- 2024/10/07:
  - 数据更新：
    - 更新了宏观经济数据
    - 增加了70城房价指数和不含在校生的失业率

- 2024/08/20：
  - 数据更新：更新了宏观经济数据

- 2024/08/09：
  - 数据更新：更新了宏观经济数据
  - 功能更新：增加了Github Actions，每日更新Tushare和yield curve数据

- 2024/07/01：
  - 数据更新：更新了股票市场数据
  - 功能更新：增加了债券收益率曲线数据，来自财政部

- 2024/06/21：
  
  - 数据更新：更新5月宏观经济数据

- 2024/06/20：
  
  - 数据更新：
    - 由于choice软件异常，5月宏观数据暂未更新
    - 更新了最新的股票相关数据，来自tushare
  - 功能更新：增加了股票市场分析模块

- 2024/06/09：
  
  - 数据更新：更新进出口基本.xlsx和进出口国家.xlsx
  - 功能更新：在进出口分析增加了播放饼图动画的按钮
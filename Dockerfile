FROM ubuntu:jammy
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai
CMD ["/bin/bash"]

RUN apt update && apt install ca-certificates -y
COPY sources.list /etc/apt/sources.list
# 安装必要的工具
RUN apt-get update && apt-get install -y \
    wget \
    sudo \
    iptables \
    ufw

# 安装conda环境到/opt/miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda3_latest.sh && \
    chmod +x miniconda3_latest.sh && \
    ./miniconda3_latest.sh -b -p /opt/miniconda && \
    echo "export PATH=/opt/miniconda/bin:\$PATH" >> ~/.bashrc

# 配置 Miniconda 的环境变量
ENV PATH="/opt/miniconda/bin:${PATH}"

# 复制依赖文件并安装 Python 包
COPY requirements.txt /root/
RUN /opt/miniconda/bin/pip install -r /root/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
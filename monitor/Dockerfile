FROM python:3.7

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 这两行是在系统钟安装了MySQL的连接器
# updata太慢 设置镜像源
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
&& apt-get clean  \
    && apt-get update  \
    && apt-get install python3-dev default-libmysqlclient-dev -y

# 创建 code 文件夹并将其设置为工作目录
RUN mkdir /code
WORKDIR /code

# 将 requirements.txt 复制到容器的 code 目录
ADD requirements.txt /code/
# 更新 pip 并 安装依赖库
RUN  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install pip -U && pip install -r requirements.txt
# 将当前目录复制到容器的 code 目录
ADD . /code/

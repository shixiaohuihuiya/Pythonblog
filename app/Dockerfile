
# 使用官方的Python运行时作为父镜像
FROM python:3.9

# 设置工作目录为/app
WORKDIR /app

# 将当前目录内容复制到容器的/app内
COPY . /app

# 安装任何需要的包
RUN pip install --no-cache-dir -r requirements.txt

# 对外暴露的端口
# EXPOSE 6789
# ENV FLASK_APP=manage.py
# ENV FLASK_RUN_HOST = 0.0.0.0
# 在容器启动时运行flask app
CMD ["python", "manage.py"]


# 1.设置工作目录   2.将工作目录的内容复制到容器中   3.下载需要的安装包   4.对外设置暴露的端口    5.运行docker容器 里面的flask
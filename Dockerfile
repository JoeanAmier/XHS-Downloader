FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到工作目录
COPY . /app

# 创建并激活虚拟环境
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# 安装依赖包
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 添加启动脚本并赋予执行权限
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# 在容器启动时执行的命令
CMD ["/app/start.sh"]

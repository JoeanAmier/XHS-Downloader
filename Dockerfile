FROM python:3.12.4-slim

LABEL name="XHS-Downloader" version="2.1" authors="JoeanAmier"

COPY locale /locale
COPY source /source
COPY static /static
COPY LICENSE /LICENSE
COPY main.py /main.py
COPY requirements.txt /requirements.txt

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["python", "main.py", "server"]

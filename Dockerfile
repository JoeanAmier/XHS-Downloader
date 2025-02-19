FROM python:3.12-slim

WORKDIR /app

LABEL name="XHS-Downloader" authors="JoeanAmier" repository="https://github.com/JoeanAmier/XHS-Downloader"

COPY locale /app/locale
COPY source /app/source
COPY static/XHS-Downloader.tcss /app/static/XHS-Downloader.tcss
COPY LICENSE /app/LICENSE
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

VOLUME /app

EXPOSE 6666

CMD ["python", "main.py"]

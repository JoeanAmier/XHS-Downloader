FROM python:3.12.4-slim

LABEL name="XHS-Downloader" version="2.2 Beta" authors="JoeanAmier"
ENV TZ Asia/Shanghai

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["python", "main.py"]
FROM python:3.12.4-slim

LABEL name="XHS-Downloader" authors="JoeanAmier" repository="https://github.com/JoeanAmier/XHS-Downloader"

COPY locale /locale
COPY source /source
COPY static /static
COPY LICENSE /LICENSE
COPY main.py /main.py
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]

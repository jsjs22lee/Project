FROM python:3.10

WORKDIR /app

# Flask 등 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt   

COPY . .                           # main.py, scheduler.py 복사

CMD ["python", "main.py"]         # Flask 서버 실행 명령

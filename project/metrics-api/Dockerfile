FROM python:3.10-slim              # Python 기반 슬림 이미지 사용

WORKDIR /app                       # 작업 디렉토리 설정

COPY requirements.txt ./          # requirements.txt 복사
RUN pip install --no-cache-dir -r requirements.txt   # Flask 등 패키지 설치

COPY . .                           # main.py, scheduler.py 복사

CMD ["python", "main.py"]         # Flask 서버 실행 명령


FROM --platform=linux/amd64 python:3.9.7
WORKDIR /app

COPY requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "${HOST_PORT}", "--port","${APP_PORT}","--reload"]


    
FROM --platform=linux/amd64 python:3.9.7
RUN pip install --upgrade pip
WORKDIR /api

COPY requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--reload"]


    
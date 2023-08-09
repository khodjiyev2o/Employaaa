# Meduzzen
Service for employee knowledge control .



## Getting Started

1. Clone the project from the Github repo :

````
git clone https://github.com/khodjiyev2o/Meduzzen
````
2. Go to the project directory  

3. Create virtual environment :

````
python3 -m venv venv
````

4. Activate virtual environment  : 

````
source\venv\bin\activate

````
if you are using Windows ,then :
````
venv\Scripts\activate
````

3.Run the server 
````
$ uvicorn main:app --reload
````
````--reload```` flag makes the server restart after code changes. Only use for development.
##How to run an application in Docker container 

1.Build  FastAPI image:

```
docker build -t fastapi .
```

2.Run a container based on the image:

```
docker run -d --name mycontainer -p 8080:8080 fastapi

```

##How to run an application in docker-compose file :

1.Build and pull  all the necessary images:
```
docker-compose build
```
2.Run the container based on the images :
```
docker-compose up

```




##How to make migrations using SqlAlchemy:

1.

```
docker-compose run api alembic revision --autogenerate -m "New Migration"
```
##new migrations should have been created in alembic/versions/. folder

2.

```
docker-compose run api alembic upgrade head
```
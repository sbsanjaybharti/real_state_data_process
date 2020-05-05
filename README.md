# Realxdata API
Flask api to push raw data into database and read the data from database.

### Requirement:
* Python
* Flask
* RabbitMA
* Celery
* MySQL
* Swagger
* docker
#### Folder Structure:
    --development(main application)
      --api
        --model(Database model)
        --service(business ligic)
        --utility(utility stuff)
        --__init__.py
        --file(routing with controller)
        --portfolio(routing with controller)
      --static
      --test
      --run.py(main file to run application)
    --mysql(For database)
    --mysql_dumps( to keep baackup of database)
    --nginx
    --rabbit(rabbitMQ)
    --traefik.toml(to monitor the trafic with list of url)
#### Step-1
1. Install Docker 
2. git clone https://github.com/sbsanjaybharti/realxdata.git if access provided else unzip the folder
3. Oper the terminal in the folder and run the command<br/>
    a. docker-compose build command<br/>
    b. docker-compose up

#### Step-2
1. open the link http://localhost:8080/ here you will get the link url like app, database, queue.
2. You can use the url provided or IP link in right, 
3. For application click on http://dev.docker.localhost/


#### Step-3 Database setup
1. Open the link http://phpmyadmin.docker.localhost
2. Username: root, password: root
3. create database realxdata
4. on the terminal follow the command
5. docker-compose exec development /bin/bash
6. python run.py db init
7. python run.py db migrate
8. python run.py db upgrade

#### Step-4
1. Open one more terminal to test, unittest testing.
2. Go to the container by command docker-compose exec development /bin/bash
3. Follow the python command:
    4. python run.py test
 
#### Description:
#####1. Design pattern:
        a. Creational: Builder, Factory and Prototype design pattern
        b. Structural: Proxy and Bridge design pattern
        c. Behaviral: Mediator and Chain of responsibility design pattern
#####2.Architecture:
        MVC architecture, Broker  Architecture pattern
 
##### Feature:
1. Celery is used to sending data to queue so that working can divide to multiple worker or server
2. Panda library is used  to handle big data to process CSV.
3. Swagger to display the API.
4. Application can handle large number of data without user waiting time.

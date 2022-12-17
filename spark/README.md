## SPARK ##

### Create Spark Container  
 
 $ docker-compose up -d

### Create MySQL Container

 $ docker run --name mysql-de9 --network=default_network --hostname mysql -e MYSQL_ROOT_PASSWORD=admin -p 3306:3306 -d mysql

### Create PostgreSQL Container

 $ docker run --name postgres-de9 --network=default_network -e POSTGRES_PASSWORD=admin -p 5445:5432 -d postgres

### CSV TO MYSQL ##
 
 # Entering Spark Container
   $ docker exec -it spark_spark-worker_1 bash

 # Copy mysql-connector-java-8.0.23.jar from folder app/package to folder jars

   $ cp mysql-connector-java-8.0.23.jar /opt/bitnami/spark/jars/  

 # Copy postgresql-42.2.18.jar from folder app/package to folder jars

   $ cp postgresql-42.2.18.jar /opt/bitnami/spark/jars/

 # Go to App folder where python file is located
   
   $ cd\
   $ cd /usr/local/spark/app

 # Start running python
 
   $ python import_csv_to_mysql.py

### MYSQL TO POSTGRESQL ###

 # Start running python
  
   $ python export_mysql_to_postgresql.py

### MONGODB TO POSTGRESQL ###
 
 # Start running python

   $ python export_mysql_to_postgresql.py


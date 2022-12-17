from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("MyApp") \
    .getOrCreate()

df1 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql:3306/sys") \
    .option("user", "root") \
    .option("password", "admin") \
    .option("dbtable", "home_credit_default_risk_application_test") \
    .load()

df1.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres-de9:5432/postgres") \
    .option("user", "postgres") \
    .option("password", "admin") \
    .option("dbtable", "home_credit_default_risk_application_test") \
    .mode("overwrite") \
    .save()

df2 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql:3306/sys") \
    .option("user", "root") \
    .option("password", "admin") \
    .option("dbtable", "home_credit_default_risk_application_train") \
    .load()

df2.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres-de9:5432/postgres") \
    .option("user", "postgres") \
    .option("password", "admin") \
    .option("dbtable", "home_credit_default_risk_application_train") \
    .mode("overwrite") \
    .save()    
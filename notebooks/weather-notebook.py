# Databricks notebook source
from pyspark.sql.functions import col

# COMMAND ----------

def load(path):
  return (spark.read
    .format("csv")
    .option("header", True)
    .schema("date DATE, temp INTEGER")
    .load(path))

# COMMAND ----------

low_df = load("/databricks-datasets/weather/low_temps")
high_df = load("/databricks-datasets/weather/high_temps")

# COMMAND ----------

joint_df = (low_df
  .select("date", 
    col("temp").alias("high_temp")
  ).join(high_df
    .select("date", 
      col("temp").alias("low_temp")
    ), ['date'], how="inner"))

# COMMAND ----------

display(joint_df.summary())

# COMMAND ----------

display(joint_df)

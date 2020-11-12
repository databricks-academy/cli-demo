# Databricks notebook source
from weather import temp

# COMMAND ----------

Temp = temp.Temperature(spark=spark, low_path="/databricks-datasets/weather/low_temps", high_path="/databricks-datasets/weather/high_temps")

# COMMAND ----------

try:
  Temp.joint_df
except AttributeError:
  print("Run .join() method to create joint_df")

# COMMAND ----------

Temp.join()

# COMMAND ----------

Temp.report(Temp.joint_df)

# COMMAND ----------

display(Temp.joint_df)

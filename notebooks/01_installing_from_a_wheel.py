# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC 
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # Installing from a Wheel
# MAGIC 
# MAGIC In this guided lab, we'll walk through the process of moving from a notebook or cluster-scoped Wheel execution to a relative import.

# COMMAND ----------

# MAGIC %md
# MAGIC If the wheel is already installed on your cluster, the following code should run.

# COMMAND ----------

from weather import temp

# COMMAND ----------

# MAGIC %md
# MAGIC If not, you can use a relative pip install to install it from within this directory.
# MAGIC 
# MAGIC **NOTE**: The python interpreter is restarted whenever a `%pip install` is run, clearing all variables in the current scope.

# COMMAND ----------

# MAGIC %pip install ../wheel/weather-1.0.0-py3-none-any.whl

# COMMAND ----------

# MAGIC %md
# MAGIC Now we can import our module.

# COMMAND ----------

from weather import temp

# COMMAND ----------

# MAGIC %md
# MAGIC You take over maintenance of a notebook that has the following logic.

# COMMAND ----------

Temp = temp.Temperature(spark=spark, low_path="/databricks-datasets/weather/low_temps", high_path="/databricks-datasets/weather/high_temps")

# COMMAND ----------

try:
    Temp.joint_df
except AttributeError:
    raise(AttributeError("Run .join() method to create joint_df"))

# COMMAND ----------

Temp.join()

# COMMAND ----------

Temp.report(Temp.joint_df)

# COMMAND ----------

display(Temp.joint_df)

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC ## Updating the Code
# MAGIC 
# MAGIC While this pattern will work in production, perhaps we'd like to update the code in our `temp` function.
# MAGIC 
# MAGIC Specifically, we've decided that we want our `.report()` method to always print out the summary statistics and preview for our `joint_df`.
# MAGIC 
# MAGIC Doing this with a Wheel would require that we completely rebuild the wheel file prior to testing the results.
# MAGIC 
# MAGIC Start by reviewing how our code is stored.

# COMMAND ----------

# MAGIC %sh ls ../wheel

# COMMAND ----------

# MAGIC %md
# MAGIC The weather module is nested within the `wheel` directory. By adding the `wheel` dir to our path, we'll be able to directly import it.
# MAGIC 
# MAGIC **NOTE**: Make sure you clear your notebook state before continuing.

# COMMAND ----------

import sys
import os

sys.path.append(os.path.abspath('../wheel'))

# COMMAND ----------

# MAGIC %md
# MAGIC Now we can directly import and use the file.

# COMMAND ----------

from weather import temp

Temp = temp.Temperature(spark=spark, low_path="/databricks-datasets/weather/low_temps", high_path="/databricks-datasets/weather/high_temps")

Temp.report()

# COMMAND ----------

# MAGIC %md
# MAGIC Let's go ahead and edit the logic to change how the `report()` method works.
# MAGIC 
# MAGIC **NOTE**: After editing, we'll need to clear the notebook state to pick up changes.

# COMMAND ----------

Temp.join()
Temp.report()

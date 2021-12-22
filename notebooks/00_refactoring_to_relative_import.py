# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC 
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md 
# MAGIC # Refactoring `%run` to a Relative Import
# MAGIC 
# MAGIC Users that use Databricks notebooks for code development and production workloads are likely aware of the `%run` magic command. This command can be used to run another notebook's code within the same scope as the calling notebook, allowing objects such as functions, variables, and classes to be reused with common setup scripts. 
# MAGIC 
# MAGIC In this lesson, we're going to use this command to run a notebook which contains a class definition in Python, then go through the process of refactoring our code to instead use relative imports with Databricks Repos.
# MAGIC 
# MAGIC ## Learning Objectives
# MAGIC By the end of this lesson, students will be able to:
# MAGIC - Describe default execution of `%run`

# COMMAND ----------

# MAGIC %md
# MAGIC ## Starting with something familiar
# MAGIC 
# MAGIC Before the ability to bring non-notebook files into Databricks feature became available, you likely might have seen code that uses a `%run` magic command. This would run another notebook and bring all code from that notebook into the namespace of the notebook where the `%run` originated from. 

# COMMAND ----------

# MAGIC %run ./helpers/weather

# COMMAND ----------

# MAGIC %md 
# MAGIC Now that we've used that, we could create our class.

# COMMAND ----------

todays_temp = Temperature(spark=spark,
                         low_path="/databricks-datasets/weather/low_temps", 
                         high_path="/databricks-datasets/weather/high_temps")

# COMMAND ----------

todays_temp.join()

# COMMAND ----------

# MAGIC %md
# MAGIC While Databricks notebooks will all support this functionality, some users may wish to write and manage code in a way closer to their local laptop experience. 
# MAGIC 
# MAGIC Let's try to import another Python class, but this time, we'll do so from inside of the helpers folder in a `.py` file.

# COMMAND ----------

# MAGIC %md 
# MAGIC ## Refactor the Relative Import
# MAGIC 
# MAGIC It might be the case that we want to use another python file for imports. Instead, we can just import from another file. Let's see what that looks like.
# MAGIC 
# MAGIC We'll note that alongside the `weather_nb` used above is a `weather.py` file.

# COMMAND ----------

# MAGIC %sh ls

# COMMAND ----------

# MAGIC %sh ls ./helpers

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC From this, we can do a relative import, similar to how we would import on a laptop.
# MAGIC 
# MAGIC **NOTE**: This is the same Python class we previously imported with `%run`. Clear the notebook state before executing the next cell if you want to confirm relative imports are working.

# COMMAND ----------

from helpers.weather_new import Temperature

# COMMAND ----------

# MAGIC %md
# MAGIC Note that while this notebook is a Python file, relative imports will only work if the `.py` extension appears here.
# MAGIC 
# MAGIC We can copy the file contents to a new file and accomplish this.

# COMMAND ----------

todays_temp = Temperature(spark=spark,
                         low_path="/databricks-datasets/weather/low_temps", 
                         high_path="/databricks-datasets/weather/high_temps")

# COMMAND ----------

todays_temp

# COMMAND ----------

# MAGIC %md 
# MAGIC ## Appending to System Path
# MAGIC 
# MAGIC Lastly, the current working directory in the Repo is included in the Python path. If you are working in a Repo root all imports for modules in the root directory and its sub directories will work.
# MAGIC 
# MAGIC If you are working in a subdirectory in the Repo and want to import modules from outside that directory you will need to append them to sys.path first. This can be done via the following Python command.

# COMMAND ----------

import sys
sys.path

# COMMAND ----------

import os
sys.path.append(os.path.abspath('../wheel'))

# COMMAND ----------

sys.path

# COMMAND ----------

# Import now that we've appended to path
from weather.temp import Temperature

# COMMAND ----------

todays_temp = Temperature(spark=spark,
                         low_path="/databricks-datasets/weather/low_temps", 
                         high_path="/databricks-datasets/weather/high_temps")

# COMMAND ----------

# MAGIC %md But that's not it. We could import from another repo as well! Let's clone the same repository with a new name `cli-demo-2`

# COMMAND ----------

# MAGIC %sh ls ../..

# COMMAND ----------

# MAGIC %md 
# MAGIC From this, we see that our relative import will come from a directory two levels above our current working directory. We can add this to our our path:

# COMMAND ----------

# MAGIC %sh pwd

# COMMAND ----------

username = spark.sql("SELECT current_user()").collect()[0][0]
print(username)

# COMMAND ----------

# Number 1.) Absolute add
import sys
sys.path.append(f"/Workspace/Repos/{username}/cli-demo-2")

# COMMAND ----------

# Profit
from wheel.weather.temp import Temperature

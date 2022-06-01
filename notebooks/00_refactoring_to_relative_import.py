# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC 
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md 
# MAGIC # Refactoring `%run` to Use a Relative Import
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

# MAGIC %run ./helpers/weather_nb

# COMMAND ----------

# MAGIC %md 
# MAGIC Now that we've used that, we could create our class.

# COMMAND ----------

todays_temp = Temperature_NB(spark=spark,
                             low_path="/databricks-datasets/weather/low_temps", 
                             high_path="/databricks-datasets/weather/high_temps")
print(todays_temp)

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
# MAGIC It might be the case that we want to use another python file for imports. 
# MAGIC 
# MAGIC Instead, we can just import from another file. 
# MAGIC 
# MAGIC First, let's take a look at what our current working directory is.

# COMMAND ----------

# MAGIC %sh pwd

# COMMAND ----------

# MAGIC %md Next, let's take a look at the contents of the current directory

# COMMAND ----------

# MAGIC %sh ls ./

# COMMAND ----------

# MAGIC %md 
# MAGIC Lastly, let's take a look at the contents of the `helpers` folder.
# MAGIC 
# MAGIC We'll note that alongside the `weather_nb` used above is a `weather.py` file.

# COMMAND ----------

# MAGIC %sh ls ./helpers

# COMMAND ----------

# MAGIC %md
# MAGIC <img src="https://files.training.databricks.com/images/icon_warn_24.png"> <b>WARNING</b>: While the contents of `weather.py` and `weather_nb` may look identical (short of the change to the class name), if you look at <a href="https://github.com/databricks-academy/cli-demo/blob/published/notebooks/helpers/weather_nb.py" target="_new"> weather_nb.py</a> in GitHub, you will see a special comment (along with some others) that clearly establishes this python file as a notebook.

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC Knowing this, we can do a relative import, similar to how we would import on a laptop.
# MAGIC 
# MAGIC **NOTE**: This is the same Python class we previously imported with `%run`.

# COMMAND ----------

from helpers.weather import Temperature_PY

# COMMAND ----------

todays_temp = Temperature_PY(spark=spark,
                             low_path="/databricks-datasets/weather/low_temps", 
                             high_path="/databricks-datasets/weather/high_temps")
print(todays_temp)

# COMMAND ----------

# MAGIC %md
# MAGIC A natural conclusion would be that we can have simply imported the notebook (which is technically a Python file) using the same technique.
# MAGIC 
# MAGIC But you can see in the cell below that this will only work for Python **files** and not Python **notebooks**.

# COMMAND ----------

try:
    from helpers.weather_nb import Temperature_NB
    
except Exception as e:
    print("Failed as expected.")
    print(e)

# COMMAND ----------

# MAGIC %md 
# MAGIC ## Appending to System Path
# MAGIC 
# MAGIC Lastly, the current working directory in the Repo is included in the Python path. 
# MAGIC 
# MAGIC If you are working in a Repo root all imports for modules in the root directory and its sub directories will work.
# MAGIC 
# MAGIC If you are working in a subdirectory in the Repo and want to import modules from outside that directory you will need to append them to sys.path first. 
# MAGIC 
# MAGIC This can be done via the following Python command.

# COMMAND ----------

import sys

for path in sys.path:
    print(path)

# COMMAND ----------

import os
sys.path.append(os.path.abspath('../wheel'))

# COMMAND ----------

for path in sys.path:
    print(path)

# COMMAND ----------

# MAGIC %md Now that the path has been updated, we can import a third version of Temperature

# COMMAND ----------

from weather.temp import Temperature

# COMMAND ----------

todays_temp = Temperature(spark=spark,
                          low_path="/databricks-datasets/weather/low_temps", 
                          high_path="/databricks-datasets/weather/high_temps")
print(todays_temp)

# COMMAND ----------

# MAGIC %md But that's not all.
# MAGIC 
# MAGIC We could import from another repo as well!
# MAGIC 
# MAGIC Let's clone the same repository with a new name `cli-demo-2`

# COMMAND ----------

# MAGIC %sh ls ../..

# COMMAND ----------

# MAGIC %md 
# MAGIC In the previous command, we see that our relative import will come from a directory two levels above our current working directory. 
# MAGIC 
# MAGIC Let's take another look at our current working directory

# COMMAND ----------

# MAGIC %sh pwd

# COMMAND ----------

# MAGIC %md We can use this information to build a new path.
# MAGIC 
# MAGIC We can start by getting our current username as seen below.

# COMMAND ----------

username = spark.sql("SELECT current_user()").first()[0]
print(username)

# COMMAND ----------

# MAGIC %md We can then use our `username` to update a new path to `sys.path`

# COMMAND ----------

import sys
sys.path.append(f"/Workspace/Repos/{username}/cli-demo-2")

# COMMAND ----------

# MAGIC %md And from there, we can import the `Temperature` object from `wheel.weather.temp`

# COMMAND ----------

from wheel.weather.temp import Temperature

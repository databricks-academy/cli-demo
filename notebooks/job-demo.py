# Databricks notebook source
from time import sleep

dbutils.widgets.text("param1", "default")
param1 = dbutils.widgets.get("param1")
sleep(20)
dbutils.notebook.exit(f"param1 passed as {param1}")

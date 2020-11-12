from pyspark.sql.session import SparkSession
from pyspark.sql.functions import col

class Temperature:
    def __init__(self, spark: SparkSession, low_path: str, high_path: str):
        self.spark = spark
        self.low_df = self.load(low_path)
        self.high_df = self.load(high_path)
        
    def load(self, path):
        return (self.spark.read
            .format("csv")
            .option("header", True)
            .schema("date DATE, temp INTEGER")
            .load(path))
            
    def join(self):
        self.joint_df = (self.low_df
            .select("date", 
                col("temp").alias("high_temp")
            ).join(self.high_df
                .select("date", 
                    col("temp").alias("low_temp")
                ), ['date'], how="inner"))
                
    def report(self, df):
        df.summary().show()
        df.limit(10).show()

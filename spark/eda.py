from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("OlistEDA") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Load data
orders = spark.read.csv("data/raw/olist_orders_dataset.csv", header=True, inferSchema=True)
customers = spark.read.csv("data/raw/olist_customers_dataset.csv", header=True, inferSchema=True)
items = spark.read.csv("data/raw/olist_order_items_dataset.csv", header=True, inferSchema=True)

print(f"Total orders: {orders.count()}")
print(f"Total customers: {customers.count()}")

# EDA 1: order status breakdown
print("\n--- Order Status Breakdown ---")
orders.groupBy("order_status").count().orderBy("count", ascending=False).show()

# EDA 2: null check
print("\n--- Null Check on Orders ---")
for col_name in orders.columns:
    null_count = orders.filter(F.col(col_name).isNull()).count()
    if null_count > 0:
        print(f"{col_name}: {null_count} nulls")

# EDA 3: RFM feature engineering
print("\n--- Building RFM Features ---")
orders_clean = orders.withColumn(
    "order_date", F.to_date("order_purchase_timestamp")
).filter(F.col("order_status") == "delivered")

max_date = orders_clean.agg(F.max("order_date")).collect()[0][0]
print(f"Latest order date: {max_date}")

rfm = orders_clean \
    .join(customers, "customer_id") \
    .join(items, "order_id") \
    .groupBy("customer_unique_id") \
    .agg(
        F.datediff(F.lit(max_date), F.max("order_date")).alias("recency"),
        F.count("order_id").alias("frequency"),
        F.round(F.avg("price"), 2).alias("monetary")
    )

rfm.show(10)
print(f"RFM rows: {rfm.count()}")

# Save as Parquet
rfm.write.mode("overwrite").parquet("data/processed/rfm_features")
print("\nDone. RFM saved to data/processed/rfm_features")

spark.stop()
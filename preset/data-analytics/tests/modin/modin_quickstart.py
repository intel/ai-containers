import modin.pandas as pd
import pandas


import time
import ray
ray.init()

# Link to raw dataset: https://modin-datasets.s3.amazonaws.com/testing/yellow_tripdata_2015-01.csv (**Size: ~200MB**)
import urllib.request
s3_path = "https://modin-datasets.s3.amazonaws.com/testing/yellow_tripdata_2015-01.csv"
urllib.request.urlretrieve(s3_path, "/home/dev/data/taxi.csv")  


start = time.time()

pandas_df = pandas.read_csv("/home/dev/data/taxi.csv", parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"], quoting=3)

end = time.time()
pandas_duration = end - start
print("Time to read with pandas: {} seconds".format(round(pandas_duration, 3)))


start = time.time()

modin_df = pd.read_csv("/home/dev/data/taxi.csv", parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"], quoting=3)

end = time.time()
modin_duration = end - start
print("Time to read with Modin: {} seconds".format(round(modin_duration, 3)))

print("## Modin is {}x faster than pandas at `read_csv`!".format(round(pandas_duration / modin_duration, 2)))

# # Faster Append with Modin's ``concat``


N_copies= 100
start = time.time()

big_pandas_df = pandas.concat([pandas_df for _ in range(N_copies)])

end = time.time()
pandas_duration = end - start
print("Time to concat with pandas: {} seconds".format(round(pandas_duration, 3)))



start = time.time()

big_modin_df = pd.concat([modin_df for _ in range(N_copies)])

end = time.time()
modin_duration = end - start
print("Time to concat with Modin: {} seconds".format(round(modin_duration, 3)))

print("### Modin is {}x faster than pandas at `concat`!".format(round(pandas_duration / modin_duration, 2)))

big_modin_df.info()


# ## Faster ``apply`` over a single column
# 
# The performance benefits of Modin becomes aparent when we operate on large gigabyte-scale datasets. For example, let's say that we want to round up the number across a single column via the ``apply`` operation. 


start = time.time()
rounded_trip_distance_pandas = big_pandas_df["trip_distance"].apply(round)

end = time.time()
pandas_duration = end - start
print("Time to apply with pandas: {} seconds".format(round(pandas_duration, 3)))


# In[12]:


start = time.time()

rounded_trip_distance_modin = big_modin_df["trip_distance"].apply(round)

end = time.time()
modin_duration = end - start
print("Time to apply with Modin: {} seconds".format(round(modin_duration, 3)))

print("### Modin is {}x faster than pandas at `apply` on one column!".format(round(pandas_duration / modin_duration, 2)))

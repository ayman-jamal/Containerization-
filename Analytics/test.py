import pymongo
# # import mysql.connector

# # mydb = mysql.connector.connect(
# #                 host="localhost",
# #                 user="root",
# #                 password="password",
# #                 database="my_db"
# #                 )

# # cursor = mydb.cursor()
# # query = """ SELECT 
# #     MAX(temperature) AS max_temperature, 
# #     (SELECT day FROM temperature_data WHERE temperature_data.temperature = (SELECT MAX(temperature) FROM temperature_data) LIMIT 1) AS max_day,
# #     MIN(temperature) AS min_temperature, 
# #     (SELECT day FROM temperature_data WHERE temperature_data.temperature = (SELECT MIN(temperature) FROM temperature_data) LIMIT 1) AS min_day,
# #     AVG(CAST(temperature AS DECIMAL(5,2))) AS avg_temperature
# # FROM temperature_data;

# #     """
# # cursor.execute(query)
# # max_temperature, max_day, min_temperature, min_day, avg_temperature = cursor.fetchone()
# mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
# # print(max_temperature, max_day, min_temperature, min_day, avg_temperature)
# data = {
#                 "max_temperature": max_temperature,
#                 "max_day": max_day.strftime("%m/%d/%Y"),
#                 "min_temperature": min_temperature,
#                 "min_day": min_day.strftime("%m/%d/%Y"),
#                 "avg_temperature": str(avg_temperature),
#             }
# # print(data)
# # # mongo_db = mongo_client['my_db']
# # # mongo_collection = mongo_db['temperature_stats']

# # # mydict = { "name": "John", "address": "Highway 37" }

# # # mongo_collection.insert_one(mydict)
from analytics import Analysis
import time

analysis = Analysis()
print(analysis.get_analytics())

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["my_db"]
mongo_collection = mongo_db["temperature_stats"]

last_record = mongo_collection.find().sort([('timestamp', -1)]).limit(1)
last_record = last_record.next()
print(last_record)
if last_record:
    data = {
        "max_temperature": last_record["max_temperature"],
        "max_day": last_record["max_day"],
        "min_temperature": last_record["min_temperature"],
        "min_day": last_record["min_day"],
        "avg_temperature": last_record["avg_temperature"]
    }
else:
    data = {
        "max_temperature": 'N/A',
        "max_day": 'N/A',
        "min_temperature": 'N/A',
        "min_day": 'N/A',
        "avg_temperature": 'N/A'
    }

print(data)
# for document in last_record:
#     print(document)
#     print("***********")
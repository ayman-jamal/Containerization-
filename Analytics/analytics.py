# import pymongo
# import mysql.connector
# from datetime import datetime

# # MongoDB connection


# class Analysis:

#     def __init__(self):
        

#         self.mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
#         self.mongo_db = self.mongo_client['my_db']
#         self.mongo_collection = self.mongo_db['temperature_stats']

#         self.mydb = mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="password",
#                 database="my_db"
#                 )

#     def get_analytics(self):
#         cursor = self.mydb.cursor()
#         query = """ SELECT 
#                     MAX(temperature) AS max_temperature, 
#                     (SELECT day FROM temperature_data WHERE temperature_data.temperature = (SELECT MAX(temperature) FROM temperature_data) LIMIT 1) AS max_day,
#                     MIN(temperature) AS min_temperature, 
#                     (SELECT day FROM temperature_data WHERE temperature_data.temperature = (SELECT MIN(temperature) FROM temperature_data) LIMIT 1) AS min_day,
#                     AVG(CAST(temperature AS DECIMAL(5,2))) AS avg_temperature
#                     FROM temperature_data; """
#         cursor.execute(query)
#         max_temperature, max_day, min_temperature, min_day, avg_temperature = cursor.fetchone()
#         data = {
#                 "max_temperature": max_temperature,
#                 "max_day": max_day.strftime("%m/%d/%Y"),
#                 "min_temperature": min_temperature,
#                 "min_day": min_day.strftime("%m/%d/%Y"),
#                 "avg_temperature": str(avg_temperature),
#             }
#         self.mongo_collection.delete_many({})
#         self.mongo_collection.insert_one(data)
#         cursor.close()
        

#         return data
            
import pymongo
import mysql.connector
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Analysis:

    def __init__(self):
        self.mongo_client = pymongo.MongoClient('mongodb://mongodb:27017/')
        self.mongo_db = self.mongo_client['my_db']
        self.mongo_collection = self.mongo_db['temperature_stats']

        self.mydb = mysql.connector.connect(
            host="mysql_db",
            user="root",
            password="password",
            database="my_db"
        )

    def get_analytics(self):
        try:
            cursor = self.mydb.cursor()
            query = """ SELECT 
                        MAX(temperature) AS max_temperature, 
                        (SELECT day FROM temperature_data WHERE temperature_data.temperature = (SELECT MAX(temperature) FROM temperature_data) LIMIT 1) AS max_day,
                        MIN(temperature) AS min_temperature, 
                        (SELECT day FROM temperature_data WHERE temperature_data.temperature = (SELECT MIN(temperature) FROM temperature_data) LIMIT 1) AS min_day,
                        AVG(CAST(temperature AS DECIMAL(5,2))) AS avg_temperature
                        FROM temperature_data; """
            cursor.execute(query)
            
            result = cursor.fetchone()
            if result:
                max_temperature, max_day, min_temperature, min_day, avg_temperature = result
                data = {
                    "max_temperature": max_temperature,
                    "max_day": max_day.strftime("%m/%d/%Y"),
                    "min_temperature": min_temperature,
                    "min_day": min_day.strftime("%m/%d/%Y"),
                    "avg_temperature": str(avg_temperature),
                }
                self.mongo_collection.delete_many({})
                self.mongo_collection.insert_one(data)
                logger.info(f"Data updated: {data}")
            else:
                logger.warning("No data returned from SQL query.")
            self.mydb.commit()
            cursor.close()
        except Exception as e:
            logger.error(f"An error occurred: {e}")

        return data

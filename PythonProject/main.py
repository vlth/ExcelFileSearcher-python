"""
This is the main entry point of the application
"""

import sys
import pymongo
from presenter.PresenterManager import PresenterManager


# myclient = pymongo.MongoClient()
# # create database
# mydb = myclient["mydatabase"]
# # create collection
# mycol = mydb["customers"]
# mydict = {"name": "John", "address": "Highway 37"}
# x = mycol.insert_one(mydict)
# print("inserted with id: " + x.inserted_id)

presenter_manager = PresenterManager()  # create presenter object
presenter_manager.start_application()   # start application

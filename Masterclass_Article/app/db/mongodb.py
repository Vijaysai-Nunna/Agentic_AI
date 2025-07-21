from pymongo import MongoClient 
from motor.motor_asyncio import AsyncIOMotorClient 
from dotenv import load_dotenv 
import os

load_dotenv() 
Mongo_URL = os.getenv("Mongo_URL")

sync_client = MongoClient(Mongo_URL) 
sync_db = sync_client['Resume_db'] 
sync_collection = sync_db['sampled_data']



async_client = AsyncIOMotorClient(Mongo_URL) 
async_db = async_client['Resume_db'] 
async_collection = async_db['sample_data']

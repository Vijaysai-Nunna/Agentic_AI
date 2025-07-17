from pymongo import MongoClient

mongo_url = "mongodb+srv://VijaySaiNunna07:rTWReTX759kxTJDb@resume.od8xhv2.mongodb.net/"
db_name = "Resume_db"
sampled_data = "sampled_data"

client = MongoClient(mongo_url)
database = client[db_name]
collection = database[sampled_data]

#***********************Insert one ***************************
# insert_one_data ={"Name": "Vijay Sai Nunna","age":22,"Designation":"Agentic AI developer","Salary": 100000}
# collection.insert_one(insert_one_data)

# data = collection.insert_one({
#     "Name":"Vijay Sai Nunna",
#     "Age":22,
#     "City":"Vijayawada",
#     "Salary":100000,
#     "Designation":"Agentic AI Developer",
#     "Company":"Zennial Pro"
# })

# #***********************Insert many ***************************
# data= collection.insert_many([
#     {"Name":"Gowri Ganesh","Age":23,"City":"Hyderabad","Salary":90000,"Designation":"Developer","Company":"Zennial Pro"},
#     {"Name":"Kiran","Age":24,"City":"Chennai","Salary":95000,"Designation":"Data Scientist","Company":"Zennial Pro"},
#     {"Name":"Praneeth","Age":25,"City":"Bangalore","Salary":105000,"Designation":"AI Engineer","Company":"Zennial Pro"},
#     {"Name":"Teja","Age":26,"City":"Mumbai","Salary":110000,"Designation":"Software Engineer","Company":"Zennial Pro"}
# ])
#***********************Find all***************************
# for d in collection.find():
#     print(d)

#***********************Find one***************************
# d= collection.find_one()
# print(d)
# print(collection.find_one({"Name":"Kiran"}))
# doc= collection.find_one({"Name ":"Praneeth"})
# print(doc)

#***********************Filtered*****************************
# filtered_docs = collection.find({"Salary": {"$gt": 100000}})
# for d in filtered_docs:
#     print(d)

# ***********************Nested Data****************************

# data = collection.insert_one(
#     {
#         "Name":"Pavan Kumar",
#         "Age":23,
#         "City":"Vishakhapatnam",
#         "Salary":45000,
#         "Designation":"Software Engineer",
#         "Company":"Zennial Pro",
#         "Address":{"city": "Vishakhapatnam",
#                    "State":"Andhrapradesh",
#                    "line":"At the beach road first left"}
#     }
# )  
# print(data.inserted_id)  
# ***********************nested data many****************************
# data = collection.insert_many([
#     {"Name":"Sai Teja",
#      "Age":24,
#      "Salary":50000,
#      "Designation":"Data analyst",
#      "Company":"Zennial Pro",
#      "Address":{"city":"Chennai",
#                 "State":"Tamilnadu",
#                 "line":"Near IT park"}},
#     {"Name":"Ravi teja",
#      "Age":25,
#      "Salary":30000,
#      "Designation":"telle caller",
#      "Company":"Zennial Pro",
#      "Address":{"city":"Vijayawada",
#                 "State":"Andhrapradesh",
#                 "line":"Singhnagar road"}}


# ])  
# print(data.inserted_ids) 

# ***********************Update one***************************
# data =collection.update_one(
#     {"Name":"Vijay Sai Nunna"},
#     {"$set":{"Salary":200000,"Designation":"Senior Agentic AI Developer"}}
# )
# print(data.modified_count)   

# ************************find sort**********************
# data = collection.find().sort("Salary",-1)
# for d in data:
#     print(d)

# data = collection.find().sort("Salary",1)
# for d in data:
#     print(d)

# data =collection.find({} ,{"_id":1,"Name ":1,"Designation":1})
# for d in data:
#     print(d)

#***********************Delete one***************************
# data = collection.delete_one({"Name":"Ravi teja"})
# print(data.deleted_count)

# ***********************Delete many***************************
# data = collection.delete_many({"Salary": {"$lt": 50000}})
# print(data.deleted_count)

# data = collection.delete_one({"Address.city":"Chennai"})
# print(data.deleted_count)

# data =collection.find({"Name":{"$regex":"^P"}})
# for d in data:
#     print(d)


# data = collection.find().sort("Salary",-1).limit(3)
# for d in data:
#     print(d)


# data = collection.delete_many({"Salary":{"$lt":100000}})
# print(data.deleted_count)


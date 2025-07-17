### MongoDB INTEGRATION with Python and FastAPI(using synchronous)

# Table of contents
1. Introduction.
2. MongoDB with python(using pymongo).
3. MongoDB with FastAPI(using synchronous).
4. Interview Questions.
5. Conclusion.

### 1. Introduction 
# 1.1 What is MongoDB?
# 1.2 Install and Set up the MongoDB?
# 1.3 What is FastAPI?
# 1.4 Set up the FastAPI?
# 1.5 Why use MongoDB with FastAPI

# 1.1 What is MongoDB?
MongoDB is a popular NoSQL database that stores data in a flexible, JSON-like document
format called BSON(Binary JSON). It uses collections and documents, making it ideal for
handling unstructured or semi-structured data.

# 1.2 Install and Set up the MongoDB?
-Steps to Install MongoDB Locally:
--Download MongoDB:
Go to the official website https://cloud.mongodb.com/
-Register to MongoDB account and create a cluster and Install.
Installation:
-Go ahead and Install the MongoDB Compass and connect it to the network with compass.
-Now create a Database and collection.

# 1.3 What is FastAPI?
-FastAPI is a modern, high-performance web framework for building APIs using Python.

# Why FastAPI?
-Fast execution using async/await.
-Automatic request validation with Pydantic.
-Interactive API docs.

# 1.4 Set up the FastAPI?
Steps to Set Up FastAPI:
Install FastAPI and Uvicorn (ASGI server):
--pip install fastapi uvicorn
Create a simple FastAPI app (main.py):
--from fastapi import FastAPI
 
``` python

app = FastAPI() 
@app.get("/")
def read():
    return {"message": "Hello, FastAPI!"}
```
--Run FastAPI app using Uvicorn:
-uvicorn main:app --reload
Access Docs:
 http://localhost:8000/docs
-Paste this local host in postman and test it or you can also do it in browser for testing.

# 1.5 Why use MongoDB with FastAPI?
-MongoDB’s document-oriented structure fits naturally with Python dictionaries and
FastAPI’s Pydantic models.
Both support asynchronous operations, improving performance.
Quick development cycles with minimal boilerplate.
Building scalable and real-time applications becomes easier.
Combines NoSQL flexibility with FastAPI’s speed and interactive documentation.



## 2.MongoDB with Python (Using PyMongo).

# 2.1 Installation.
# 2.2 Environment Setup.
# 2.3 Commands
# 2.4 Commands Purpose
 
# What is PyMongo?
--PyMongo is the official Python driver that lets your Python application communicate with
MongoDB. It allows you to perform CRUD operations easily from Python scripts.
 
 
# 2.1 Installation

--Install this command 
 
pip install pymongo

# 2.2 Environment Setup
--
 ``` python
from pymongo import MongoClient

mongo_url = "Your mongo url"
db_name = "Resume_db"
sampled_data = "sampled_data"

client = MongoClient(mongo_url)
database = client[db_name]
collection = database[sampled_data]

```
from pymongo import MongoClient

Import MongoClient from the pymongo library.
This is a connection between Python and MongoDB.

mongo_url: Your MongoDB connection string.

db_name: The name of your MongoDB database.

sampled_data: The collection name inside that database.

client object connects your Python code to MongoDB using the provided URL.This is like 
opening a communicate channel to your MongoDB server.

database = client[db_name]
Access the database using the client object.

Here, you're selecting your target database: "Resume_db".

collection = database[sampled_data]
Access the collection inside the database.
This collection is where you will perform operations like insert, find, update, and delete.

# 2.3 Commands
 
# 2.3.1 Insert One Document
  ``` python
data = collection.insert_one({
    "Name":"Ankith Kolekar",
    "Age":22,
    "City":"Vijayawada",
    "Salary":100000,
    "Designation":"Agentic AI Developer",
    "Company":"Zennial Pro"
 })
 ```
 
# 2.3.2 Insert Many Documents

 ``` python

data= collection.insert_many([
    {"Name":"Alice kingfor","Age":23,"City":"Hyderabad","Salary":90000
    "Designation":"Developer","Company":"Zennial Pro"},
    {"Name":"Sultan Alli","Age":24,"City":"Chennai","Salary":95000
    "Designation":"DataScientist","Company":"Zennial Pro"},
    {"Name":"Praneeth","Age":45,"City":"Bangalore","Salary":105000
    "Designation":"AIEngineer","Company":"Zennial Pro"},
    {"Name":"Teja","Age":32,"City":"Mumbai","Salary":110000
    "Designation":"SoftwareEngineer","Company":"Zennial Pro"}
])
 
```
 
# 2.3.3 Find One Document
  ``` python

doc = collection.find_one({"name": "Alice"})
print(doc)
 ```
 
# 2.3.4 Find All / Many Documents
  ``` python

for doc in collection.find():
    print(doc)
 ```
 
# 2.3.5 Filtered Find (Greater Than)

 ``` python
 
filtered_docs = collection.find({"age": {"$gt": 30}})
for doc in filtered_docs:
    print(doc)
 ```
 
# 2.3.6 Update One Document
  ``` python
data = collection.update_one(
    {"name": "John"},
    {"$set": {"age": 40}}
)
print(data.modified_count)
  ``` 
 
# 2.3.7 Delete One Document
 
 ``` python
result = collection.delete_one({"name": "Charlie"})
print(result.deleted_count)
  ```


# 2.3.8 Delete many
data = collection.delete_many({"Salary": {"$lt": 50000}})
print(data.deleted_count)

data = collection.delete_one({"Address.city":"Chennai"})
print(data.deleted_count)

# 2.3.9 Sorting Documents
 
# Sort by age ascending
 ``` python
for doc in collection.find().sort("age", 1):
    print(doc)
 
# Sort by age descending
for doc in collection.find().sort("age", -1):
    print(doc)
 ```
 
# 2.3.10 Regex Filter (Names starting with alphabets)
``` python 
data =collection.find({"Name":{"$regex":"^P"}})
for d in data:
    print(d)
```

# 2.3.11 Nested Data

``` python 
data = collection.insert_one(
    {
        "Name":"Pavan sharan",
        "Age":23,
        "City":"Vishakhapatnam",
        "Salary":45000,
        "Designation":"Software Engineer",
        "Company":"Zennial Pro",
        "Address":{"city": "Vishakhapatnam",
                   "State":"Andhrapradesh",
                   "line":"At the beach road first left"}
    }
)  
print(data.inserted_id) 

```
# 2.3.12 Nested data Many
``` python 
data = collection.insert_many([
    {"Name":"Sai Teja",
     "Age":24,
     "Salary":50000,
     "Designation":"Data analyst",
     "Company":"Zennial Pro",
     "Address":{"city":"Chennai",
                "State":"Tamilnadu",
                "line":"Near IT park"}},
    {"Name":"Ravi teja",
     "Age":25,
     "Salary":30000,
     "Designation":"telle caller",
     "Company":"Zennial Pro",
     "Address":{"city":"Vijayawada",
                "State":"Andhrapradesh",
                "line":"Singhnagar road"}}


])  
print(data.inserted_ids) 
``` 

# 2.3.13 Find sort
``` python 
data = collection.find().sort("Salary",-1)
for d in data:
    print(d)

data = collection.find().sort("Salary",1)
for d in data:
    print(d)

data =collection.find({} ,{"_id":1,"Name ":1,"Designation":1})
for d in data:
    print(d)

```
# 2.4 Commands Purpose
 ``` python  
insert_one()	Insert a single document
insert_many()	Insert multiple documents
find_one()	    Fetch a single document
find()	        Fetch multiple documents
update_one()	Update a single document
delete_one()	Delete a single document
delete_many()   Delete many document
.sort()	        Sort results (asc/desc)
nested data     contain tags with distinct entities
$regex filter	Filter documents using regex
```
------
## 3. MonogDB with FastPAI(using synchronous).
# 3.1 Installation
# 3.2 Environment setup
# 3.3 Commands  
# 3.4 API endpoints
# 3.5 How to Provide JSON in Postman with URLs
 
# What is PyMongo with FastAPI?
 
Using PyMongo in combination with FastAPI allows us to create RESTful APIs connected to a
MongoDB database using synchronous routes.
 
# 3.1 Installation
 
pip install pymongo fastapi uvicorn

# 3.2 Environment Setup
  ``` python 
from fastapi import FastAPI
from pymongo import MongoClient
 
app = FastAPI()
mongo_url = "your url"
db_name = "Resume_db"
sampled_data = "sampled_data"

client = MongoClient(mongo_url)
database = client[db_name]
collection = database[sampled_data]
 ```
# 3.3 Commands

# 3.3.1 Insert One Document

--We can insert one document by request and http link

  ``` python 
@app.post("/insert_one")
def insert_one_user(name: str, age: int):
    result = collection.insert_one({"name": name, "age": age})
    return {"inserted_id": str(result.inserted_id)}
 ```
 
# 3.3.2 Insert Many Documents
  ``` python 
@app.post("/insert_many")
def insert_many_users(users: list):
    result = collection.insert_many(users)
    return {"inserted_ids": [str(id) for id in result.inserted_ids]}
  ```
 
# 3.3.3 Find One Document
  ``` python 
@app.get("/find_one")
def find_one_user(name: str):
    result = collection.find_one({"name": name}, {"_id": 0})
    return result
  ``` 
 
# 3.3.4 Find Many Documents
 ``` python 
@app.get("/find_many")
def find_many_users():
    users = list(collection.find({}, {"_id": 0}))
    return users
  ``` 
 
# 3.3.5 Update One Document

 ``` python  
@app.put("/update_one")
def update_user(name: str, age: int):
    result = collection.update_one({"name": name}, {"$set": {"age": age}})
    return {"modified_count": result.modified_count}
 
  ```
 
# 3.3.6 Delete One Document

 ``` python 
@app.delete("/delete_one")
def delete_user(name: str):
    result = collection.delete_one({"name": name})
    return {"deleted_count": result.deleted_count}
 
 ```
 
# 3.3.6 Sorting Documents

 ``` python  
@app.get("/sort_asc")
def sort_users_asc():
    users = list(collection.find({}, {"_id": 0}).sort("age", 1))
    return users
 
@app.get("/sort_desc")
def sort_users_desc():
    users = list(collection.find({}, {"_id": 0}).sort("age", -1))
    return users
  ``` 
 
# 3.3.7 Regex Filter (Names starting with alphabets)
  ``` python
@app.get("/regex_filter")
def regex_filter_users():
    users = list(collection.find({"name": {"$regex": "^[A-Za-z]"}}, {"_id": 0}))
    return users
  ```
 
# 3.4 API Endpoints
 
Endpoint	            Purpose
/insert_one	    Insert a single document
/insert_many	Insert multiple documents
/find_one	    Fetch a single document
/find_many	    Fetch multiple documents
/update_one	    Update a single document
/delete_one	    Delete a single document
/sort_asc	    Sort results ascending
/sort_desc	    Sort results descending
/regex_filter	Filter documents using regex
 
# 3.5 How to Provide JSON in Postman with URLs
 
# 3.5.1 For /insert_one (POST Request)
-- For this we can provide json on postman
URL:http://localhost:8000/insert_one?name=John&age=30
Body: Not required (parameters sent as query parameters).

 
# 3.5.2 For /insert_many (POST Request)
URL:http://localhost:8000/insert_many
Body (raw - JSON):

[
  {"name": "Alice", "age": 25},
  {"name": "Bob", "age": 28},
  {"name": "Charlie", "age": 35}
]

# 3.5.3 For /update_one (PUT Request)
URL:http://localhost:8000/update_one?name=John&age=35
Body: Not required (parameters sent as query parameters).

# 3.5.4 For /delete_one (DELETE Request)
URL:http://localhost:8000/delete_one?name=John
Body: Not required.
 
# 3.5.5 For /find_one, /find_many, /sort_asc, /sort_desc, /regex_filter
Method: GET
Body: Not required


## 4. Interview Questions
# 4.1 MongoDB Inerview Q/A.
# 4.2 MongoDB with python Interiew Q/A.
# 43 MongoDB with fastapi async Interview Q/A

# 4.1 MongoDB: Interview Questions & Answers
1. What is MongoDB?
A) MongoDB is a NoSQL database that stores data in JSON-like documents called BSON. It is
schema-less and highly scalable.

2. What is a Collection in MongoDB?
A) A collection is equivalent to a table in SQL databases and contains multiple documents.

3. What command is used to insert a document?
A) In MongoDB, documents are inserted using the insertOne() or insertMany() commands.

4. What is BSON?
A) BSON (Binary JSON) is a binary representation of JSON documents, optimized for speed
and space, used internally by MongoDB.

5. What is the purpose of Indexing in MongoDB?
A) Indexing improves query performance by allowing the database to locate data without
scanning every document.

6. What is the difference between find() and findOne()?
A) find() retrieves multiple documents.
findOne() retrieves the first matching document.

# 4.2 MongoDB with Python (PyMongo): Interview Questions & Answers
1. What is PyMongo?
A) PyMongo is the official Python driver that allows Python applications to interact with
MongoDB databases.

2. How do you connect MongoDB with Python?
A) Using MongoClient from the pymongo library:
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')

3. How to insert a document using PyMongo?
A) By using:
data = collection.insert_one({
    "Name":"Vijay Sai Nunna",
    "Age":22,
    "City":"Vijayawada",
    "Salary":100000,
    "Designation":"Agentic AI Developer",
    "Company":"Zennial Pro"
})

4. How to retrieve all documents from a collection?
A) By using:
for doc in collection.find():
    print(doc)

5. How to update a document in MongoDB using PyMongo?
A) By using:

data =collection.update_one(
    {"Name":"Vijay Sai Nunna"},
    {"$set":{"Salary":200000,"Designation":"Senior Agentic AI Developer"}}
)
print(data.modified_count) 

6. Can you use regex queries with PyMongo?
A) Yes. Example:
collection.find({"name": {"$regex": "^A"}})

# 4.3 MongoDB with FastAPI (Sync): Interview Questions & Answers
1. Why use FastAPI with MongoDB?
A) To build RESTful APIs that interact with MongoDB databases, providing CRUD operations
over HTTP.

2. How do you handle MongoDB operations in FastAPI sync mode?
A)By using pymongo directly inside route functions without async/await.

3. What is the role of Uvicorn in FastAPI projects?
A) Uvicorn acts as the ASGI server that serves the FastAPI application.

4. How to insert data in MongoDB using FastAPI sync?
A)Use a route like:
@app.post(\"/insert_one\")
def insert_one(name: str, age: int):
    collection.insert_one({\"name\": name, \"age\": age})

5. Can FastAPI automatically generate API documentation?
A) Yes, using Swagger UI, accessible at /docs.

6. Why prefer sync MongoDB integration in simple projects?
A) Sync (PyMongo) is easier to implement and suitable for small-scale APIs wher
 non-blocking execution isn't critical.

## 5.Conclusion
--MongoDB with Python and FastAPI (Synchronous) offers a simple, practical approach to
working with NoSQL databases using Python. By using PyMongo we can use and  perform all
CRUD operations directly from Python scripts or use them into FastAPI APIs using
synchronous routes.

--MongoDB with Python (PyMongo) is ideal for backend scripts, data processing tasks, or
simple applications where direct database interaction is required.

--MongoDB with FastAPI (Synchronous) allows you to expose database operations as RESTful
APIs efficiently using PyMongo inside FastAPI routes.

In both methods:
i)Setup is straightforward.
ii)Commands like insert_one(), find_one(), update_one(), delete_one(), and .sort() are
common and consistent.
iii)Data can be filtered using regex and sorted easily.
iv)JSON-based document storage makes data handling flexible.
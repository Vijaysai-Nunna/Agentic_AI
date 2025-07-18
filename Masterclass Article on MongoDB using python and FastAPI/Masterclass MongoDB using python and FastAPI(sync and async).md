# MongoDB Integration with Python and FastAPI(using sync and async)
## Overview:
- This learning guide focuses exclusively on MongoDB integration using Python and FastAPI,
covering both synchronous and asynchronous approaches. Code examples and conceptual
explanations are included for practical understanding.Here You'll undertand MongoDB
Basics,MongoDB using Python,MongoDB using FastAPI(Sync + Async using motor) and important
interview questions.
---
## Section 1: MongoDB Basics

### 1.1 What is MongoDB?
- MongoDB is a NoSQL database that stores data in BSON format (Binary JSON).
- Works with collections and documents, ideal for semi-structured or unstructured data.

### 1.2 Setting Up MongoDB Atlas
1. Visit https://cloud.mongodb.com
2. Create a free cluster.
3. Setup database and collection.
4.  Whitelist IP and get your connection URL.

Example .env variable:
```python
- MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/dbname
```
---

## Section 2: MongoDB with Python (Using PyMongo)

### 2.1 What is PyMongo?
- Using pymongo in database interacton inside python scripts.
- PyMongo is MongoDB's official Python driver.
- Allows Python scripts to perform simple CRUD operations(insert,Find,update,delete)
  directly.

### 2.2 Basic Setup:

```python
from pymongo import MongoClient

client = MongoClient("your_mongo_url")
db = client['Resume_db']
collection = db['sampled_data']
```
#### Explanation of Code:
from pymongo import MongoClient: 
- Import MongoClient from the pymongo library.
- This is a connection between Python and MongoDB.

#### mongo_url
- Your MongoDB connection string.
#### db_name
- The name of your MongoDB database.

#### sampled_data: 
- The collection name inside that database.
#### client = MongoClient("your_mongo_url")
- client object connects your Python code to MongoDB using the provided URL.This is like 
- opening a communicate channel to your MongoDB server.

#### database = client[db_name]
- Access the database using the client object.
- Here, you're selecting your target database: "Resume_db".

#### collection = database[sampled_data]
- Access the collection inside the database.
- This collection is where you will perform operations like insert, find, update, and
delete.

### 2.3 CRUD Examples:
#### Insert One Document:

```python
collection.insert_one({"name": "Vijay", "age": 23})
```

#### Find All Documents:
```python
for doc in collection.find():
    print(doc)
```
#### Update One Document:

```python
collection.update_one({"name": "Vijay"}, {"$set": {"age": 25}})
```
#### Delete One Document:
```PYTHON
collection.delete_one({"name": "Vijay"})
```
---
## Section 3: MongoDB with FastAPI (Using Synchronous PyMongo)

### 3.1 What is FastAPI?
- FastAPI is a modern, high-performance Python web framework specifically designed for
building APIs (Application Programming Interfaces). It's known for its speed, ease of use,
and automatic documentation generation, leveraging Python's type hinting for enhanced code
clarity and validation.

### 3.2 What is pymongo what is the use of pymongo?
- PyMongo is the official MongoDB driver for synchronous Python applications. If you want
to learn how to connect and use MongoDB from your Python application, you've come to the
right place. In this PyMongo tutorial, we'll build a simple CRUD (Create, Read, Update,
Delete) application using FastAPI and MongoDB Atlas.

### 3.3 What is Use of FastAPI?
- FastAPI is a modern Python framework for building APIs.
- Offers auto-generated Swagger UI.
- Fast execution, simple setup.

### 3.4 FastAPI (Synchronous Mode) + MongoDB
- Expose MongoDB operations as REST API's using FastAPI.
- Routes handled synchronously.
- Simple to implement for small-sclae API's

- Setup:
```python
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()
client = MongoClient("your_mongo_url")
db = client['Resume_db']
collection = db['sampled_data']
```
### API Endpoints:

#### Insert Document:
```python
@app.post("/insert")
def insert(name: str, age: int):
    collection.insert_one({"name": name, "age": age})
    return {"message": "Inserted"}
```
#### Find Documents:
```python
@app.get("/users")
def get_users():
    return list(collection.find({}, {"_id": 0}))
```
#### 3.5 Running:
```python
uvicorn app:app --reload
```
Swagger UI at: http://localhost:8000/docs

---
## Section 4: MongoDB with FastAPI Async (Using Motor)

### 4.1 Why Async? (ASGI Framework)
- Non-blocking request handling.
- Better for concurrent operations.
- Uses async/await syntax.

### 4.2 Motor Library
- Use motor for non-blocking asynchronous database operations.
- Motor is the async driver for MongoDB in Python.
- Works seamlessly with FastAPI.

#### Installation:
```python
pip install motor fastapi uvicorn
```
#### Async Example Setup:
```python
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()
client = AsyncIOMotorClient("your_mongo_url")
db = client['Resume_db']
collection = db['sampled_data']

class Person(BaseModel):
    name: str
    age: int
```
#### Async Endpoint Example:
```python 
@app.post("/insert-async")
async def insert_async(name: str, age: int):
    await collection.insert_one({"name": name, "age": age})
    return {"message": "Inserted asynchronously"}
```
#### Fetch Documents Asynchronously:
```python
@app.get("/users-async")
async def get_users_async():
    users = []
    cursor = collection.find({}, {"_id": 0})
    async for document in cursor:
        users.append(document)
    return users
 ```
---
## Section 5: Sync vs Async Explained

| Feature| FastAPI + Pymongo(Sync) | FastAPI + Motor(Async) |
|-----------|----------------|-----------------|
| Architecture |WSGI (Blocking)  | ASGI (Non-blocking) |
| Request | Handling Blocking | Non-blocking |
| Performance | Limited concurrency | High concurrency |
| Syntax | Simple functions | async/await needed |
| Scalability | Limited | High |


### Example Comparison:

#### Synchronous:
```python
@app.get("/sync-example")

def sync_task():
    data = collection.find_one({"name": "Vijay"})
    return data
```
#### Asynchronous:
```python
@app.get("/async-example")

async def async_task():
    data = await collection.find_one({"name": "Vijay"})
    return data
```
---

## Section 6: Interview Preparation Questions
### MongoDB — Interview Questions
Q1. What is MongoDB?

Q2. What is the difference between a Collection and a Document?

Q3. Why is MongoDB preferred over SQL for modern applications?

Q4. How does indexing work in MongoDB?

Q5. How can you connect MongoDB to a cloud cluster?

Q6. What is MongoDB and what format does it use for storing data?

Q7. Explain collections and documents in MongoDB?

Q8. What is BSON?

Q9. Why use MongoDB Atlas?

---
### MongoDB with Python (PyMongo) — Interview Questions
Q1. What is PyMongo?

Q2. How do you establish a connection using PyMongo?

Q3. How do you insert a single document in PyMongo?

Q4. How to retrieve all documents from a collection?

Q5. How can you update data in PyMongo?

Q6. Can PyMongo handle regex filtering?

---
### MongoDB with FastAPI (Synchronous - PyMongo) — Interview Questions
Q1. Why use PyMongo with FastAPI?

Q2. How is synchronous CRUD implemented in FastAPI?

Q3. Can FastAPI auto-generate Swagger docs for APIs?

Q4. What is the role of Uvicorn in FastAPI?

Q5. When should you prefer sync MongoDB usage in FastAPI?

Q6. How to insert data in FastAPI synchronously?

---
### MongoDB with FastAPI (Asynchronous - Motor) — Interview Questions
Q1. What is Motor?

Q2. Why use async/await in FastAPI with MongoDB?

Q3. How do you perform an async insert in FastAPI using Motor?

Q4. What is the benefit of ASGI over WSGI?

Q5. Where is async CRUD useful?

Q6. How does FastAPI handle auto-documentation for async routes?

---
## Section 7: Links

Github Link: https://github.com/Vijaysai-Nunna/Agentic_AI/tree/Vijay

## Section 8: Conclusion

- MongoDB with Python (PyMongo): Ideal for backend scripts and basic CRUD.
- MongoDB with FastAPI (Synchronous): Practical for simple REST APIs without async
  complexity.
- MongoDB with FastAPI (Asynchronous using Motor): Recommended for production-grade,
  high-concurrency applications.

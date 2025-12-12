import json
import os

DB_File = "expense_data.json"

#Load existing data from json file
if os.path.exists(DB_File):
    with open(DB_File,"r") as f:
        expenses = json.load(f)
else:
    expenses = {}

#To save data to file
def save_to_file():
    with open(DB_File, "w") as f:
        json.dump(expenses, f, indent=4)
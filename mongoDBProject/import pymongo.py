import pymongo
 
# Connect to the database
client = pymongo.MongoClient('mongodb+srv://Vasavivasu:i63KCiAIZpUzWn6X@cluster0.zevtixc.mongodb.net/?retryWrites=true&w=majority')


# Connect to the 'test' database
db = client['test']
 
# Get the 'users' collection
users = db['users']
 
# Insert a single document
result = users.insert_one({
    'name': 'Jhn mith',
    'email': 'herin@gmail.com'
})
 
print(result)

cursor = users.find({'name': 'John Smith'})
 
# Iterate over the cursor and print the documents
for doc in cursor:
    print(doc)
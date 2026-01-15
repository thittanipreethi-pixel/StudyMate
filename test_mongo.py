from pymongo import MongoClient

uri = "mongodb+srv://nalliayanandhakumar_db_user:Q.8MRJ8iL5pwn%u@cluster0.uboewoe.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

try:
    db = client["studymate_db"]
    print("✅ MongoDB Connected Successfully")
    print("Collections:", db.list_collection_names())
except Exception as e:
    print("❌ MongoDB Connection Failed")
    print(e)

from pymongo import MongoClient

uri = "mongodb+srv://thittanipreethi_db_user:preethi@2006@cluster0.oepojpf.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

try:
    db = client["studymate_db"]
    print("✅ MongoDB Connected Successfully")
    print("Collections:", db.list_collection_names())
except Exception as e:
    print("❌ MongoDB Connection Failed")
    print(e)

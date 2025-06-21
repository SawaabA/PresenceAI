from pymongo import MongoClient

# Connect using your MongoDB URI
client = MongoClient("mongodb+srv://sawaabanas:slYBwTKM0FJlPnLB@cluster0.tszidan.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Select a database (MongoDB will auto-create this if it doesn't exist)
db = client["presenceAI"]

# Select a collection (MongoDB will auto-create this too)
collection = db["body_language_feedback"]

# Insert a sample test document
sample_data = {
    "user_id": "test_user",
    "speech_id": "test_speech_001",
    "hand_static_ratio": 0.77,
    "feedback": "Try to use your hands more."
}

collection.insert_one(sample_data)
print("Data inserted!")

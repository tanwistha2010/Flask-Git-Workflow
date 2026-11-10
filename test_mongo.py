from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_URI")

print("URI loaded:", bool(uri))

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)

    client.admin.command("ping")

    print("SUCCESS: MongoDB connected!")

except Exception as e:
    print("ERROR:", e)

finally:
    if uri:
        client.close()
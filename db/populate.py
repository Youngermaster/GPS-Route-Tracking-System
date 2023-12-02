from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Configuration
MONGO_URI = "mongodb://root:examplepassword@localhost:27017"
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["route_database"]

# Sample Route Document with Empty Directions
route_document = {
    "_id": ObjectId(),
    "route_id": "route-123",
    "name": "Route A-B-C-A",
    "isProcessed": False,  # Indicates that the route path is not yet created
    "isFinished": False,  # Indicates the overall route status
    "directions": [],  # Empty array to be populated with real-time data
    "polyline": [],  # Empty array to be populated with the polyline points.
}

# Inserting the Document into the Collection
db.routes.insert_one(route_document)
print("Route document inserted successfully with empty directions.")

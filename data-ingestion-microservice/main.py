import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import redis
from geopy.distance import geodesic
from datetime import datetime

# MQTT Broker, MongoDB, and Redis Configurations
MQTT_BROKER = "localhost"
MONGO_URI = "mongodb://root:examplepassword@localhost:27017"
REDIS_HOST = "localhost"

# Geofence Configuration (example coordinates and radius in meters)
GEOFENCE_CENTER = (6.1756, -75.5775)  # Example: EAFIT coordinates
GEOFENCE_RADIUS = 15  # 15m radius

# MongoDB and Redis Clients
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["route_database"]
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)


def is_inside_geofence(coord):
    return geodesic(GEOFENCE_CENTER, coord).meters <= GEOFENCE_RADIUS


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("location/rn-client")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    handle_location_data(data)


def create_trip_document(route_id, path):
    trip_document = {
        "route_id": route_id,
        "driver": "driver-123",  # Replace with actual data
        "vehicle": "vehicle-123",  # Replace with actual data
        "isFinished": True,
        "start_time": datetime.now(),  # Replace with actual start time
        "end_time": datetime.now(),  # Replace with actual end time
        "actual_path": path, # []
    }
    db.trips.insert_one(trip_document)


def handle_location_data(data):
    route_id = data.get("currentRouteId")
    location = (data["driverLocation"]["latitude"], data["driverLocation"]["longitude"])

    route = db.routes.find_one({"route_id": route_id})
    if route:
        if is_inside_geofence(location):
            path = redis_client.lrange(route_id, 0, -1)
            path = [json.loads(point.decode("utf-8")) for point in path]

            if not route.get("isProcessed"):
                # If route is not processed, update the route document
                # reduced_path = reducer(path)
                db.routes.update_one(
                    {"route_id": route_id},
                    {"$set": {"directions": path, "isProcessed": True}},
                )
            else:
                # If route is already processed, create a new trip document
                create_trip_document(route_id, path)

            redis_client.delete(route_id)
        else:
            redis_client.rpush(route_id, json.dumps(location))


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()

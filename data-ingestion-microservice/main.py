import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import redis
from geopy.distance import geodesic

# MQTT Broker, MongoDB, and Redis Configurations
MQTT_BROKER = "localhost"
MONGO_URI = "mongodb://root:examplepassword@localhost:27017"
REDIS_HOST = "localhost"

# Geofence Configuration (example coordinates and radius in meters)
GEOFENCE_CENTER = (40.7128, -74.0060)  # Example: New York City coordinates
GEOFENCE_RADIUS = 1000  # 1km radius

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


def handle_location_data(data):
    route_id = data.get("currentRouteId")
    location = (data["driverLocation"]["latitude"], data["driverLocation"]["longitude"])

    route = db.routes.find_one({"route_id": route_id})
    if route and route.get("createPath"):
        # If inside geofence and route is complete, update MongoDB and reset Redis
        if is_inside_geofence(location):
            path = redis_client.lrange(route_id, 0, -1)
            path = [json.loads(point.decode("utf-8")) for point in path]
            db.routes.update_one(
                {"route_id": route_id}, {"$set": {"path": path, "createPath": False}}
            )
            redis_client.delete(route_id)
        else:
            # Store location data in Redis
            redis_client.rpush(route_id, json.dumps(location))


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()

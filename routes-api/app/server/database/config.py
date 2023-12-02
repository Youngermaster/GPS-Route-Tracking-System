from decouple import config
import motor.motor_asyncio

MONGO_URL = config(
    "MONGO_URL",
    default="mongodb://root:examplepassword@localhost:27017/?authMechanism=DEFAULT",
)

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.route_database

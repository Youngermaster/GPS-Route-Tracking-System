from .config import database
from server.models.route import RouteSchema, ObjectIdStr

route_collection = database.get_collection("routes")

async def retrieve_route(route_id: str):
    route = await route_collection.find_one({"route_id": route_id})
    if route:
        return RouteSchema(**route)
    return None

async def retrieve_polyline(route_id: str):
    route = await route_collection.find_one({"route_id": route_id}, {"polyline": 1})
    if route:
        return route.get("polyline", [])
    return []

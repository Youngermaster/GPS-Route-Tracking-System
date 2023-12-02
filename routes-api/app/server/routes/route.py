from fastapi import APIRouter, Path
from server.database.route import retrieve_route, retrieve_polyline
from server.models.route import RouteSchema

router = APIRouter()

@router.get("/{route_id}", response_model=RouteSchema, response_description="Route data retrieved")
async def get_route_data(route_id: str = Path(..., description="The ID of the route to retrieve")):
    route = await retrieve_route(route_id)
    if route:
        return route
    return {"message": "Route not found"}

@router.get("/{route_id}/polyline", response_description="Polyline data retrieved")
async def get_polyline_data(route_id: str = Path(..., description="The ID of the route to retrieve polyline for")):
    polyline = await retrieve_polyline(route_id)
    return {"polyline": polyline}

# DB

## Database Structure: Routes and Trips

1. **Routes Collection**:
   - A `routes` collection should store the static information of each route.
   - Each route document might include the route ID, name, a set of coordinates forming the path (`LineString`), and other static data like expected time, distance, etc.

2. **Trips Collection**:
   - A separate `trips` collection should store data for individual trips taken by buses on these routes.
   - Each trip document would reference the route ID from the `routes` collection.
   - Trip-specific data might include actual start time, end time, dynamic route data (if it varies from the standard route), average speed, delays, etc.

## Data Storage Approach

1. **Creating a New Route**:
   - When a bus driver starts a new route that doesn't exist in the `routes` collection, create a new document in this collection.
   - The route document includes the polyline (sequence of GPS coordinates) and other relevant static data.
   - This route ID is then used for all future trips on this route.

2. **Storing Trip Data**:
   - For each trip, create a new document in the `trips` collection.
   - Include a reference to the route ID from the `routes` collection.
   - Store trip-specific dynamic data, such as actual times, deviations from the standard route, etc.

3. **Route Completion**:
   - Upon completion of a trip, update the trip document with end time and other relevant metrics.

## Example Document Structure

- **Route Document**:

  ```json
  {
    "_id": ObjectId("..."),
    "route_id": "route-123",
    "name": "Route A-B-C-A",
    "isProcessed": true,
    "isFinished": true,
    "directions": [
      [longitude, latitude], // Start Point A
      [longitude, latitude], // Point B
      [longitude, latitude], // Point C
      [longitude, latitude]  // End Point A
    ],
    // Other static route details...
  }
  ```

- **Trip Document**:

  ```json
  {
    "_id": ObjectId("..."),
    "route_id": "route-123", // Reference to the Route
    "driver": "driver-123", // Reference to the Driver
    "vehicle": "vehicle-123", // Reference to the Vehicle
    "isFinished": true,
    "start_time": ISODate("..."),
    "end_time": ISODate("..."),
    "actual_path": [
      // Potentially more detailed path data for this specific trip
    ],
    // Other dynamic trip details...
  }
  ```

## Best Practices

- **Data Normalization**: Keep a clear distinction between static route data and dynamic trip data to avoid redundancy.
- **References**: Use route IDs to link trips to their respective routes.
- **Query Optimization**: Index fields that are frequently queried, like `route_id` in trips.
- **Data Integrity**: Ensure data consistency between routes and trips, especially when updating route information.

## Handling Polyline Data

- When retrieving a route for display (e.g., as a polyline on a map), you can query the `routes` collection for the static path.
- For displaying an actual trip, query the `trips` collection and use the `actual_path` if it differs from the standard route.

import time
from shapely.geometry import LineString


def ramer_douglas_peucker(points, epsilon):
    """
    Simplifies a list of points using the Ramer-Douglas-Peucker algorithm.

    Args:
    - points (list of tuples): List of (latitude, longitude) points.
    - epsilon (float): The maximum distance of a point from the line for it to be retained.

    Returns:
    - list of tuples: The simplified list of points.
    """
    print("Ramer-Douglas-Peucker algorithm started")
    start_time = time.time()  # Start timer

    line = LineString(points)
    simplified_line = line.simplify(epsilon)

    end_time = time.time()  # End timer
    print(f"Ramer-Douglas-Peucker algorithm took {end_time - start_time:.6f} seconds.")

    return list(simplified_line.coords)

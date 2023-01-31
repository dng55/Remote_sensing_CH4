def lon_to_m(degree, coordinates):
    """
    degree is the single point's longitude of a spatial map
    coordinates are the flux tower coordiantes listed in [lon, lat] format
    e.g. coordinates = [-122.9849,49.1293]
    """
    Point = coordinates
    metre = (degree-Point[0])/(1/85000)
    return metre
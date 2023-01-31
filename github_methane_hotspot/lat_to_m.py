def lat_to_m(degree, coordinates):
    """
    degree is the single point's latitude of a spatial map
    coordinates are the flux tower coordiantes listed in [lon, lat] format
    e.g. coordinates = [-122.9849,49.1293]
    """
    Point = coordinates
    metre = (degree-Point[1])/(1/111000)
    return metre
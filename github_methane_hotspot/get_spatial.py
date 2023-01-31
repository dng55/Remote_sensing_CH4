def get_spatial(date, spatial_index,dataStruct,interval,coordinates):
    """
    Grabs all satellite data for a single given date
        Input: 
            1) date {int}: starting time by landsat id (format: yyymmdd. eg: 20130328)
            2) spatial_index {string}: The name of the spatial index you're looking for. All uppercase.
                    Available indices: "NDVI", "NDWI", "MNDWI_SW1", "MNDWI_SW2"
            3) dataStruct: dictionary that holds satellite data containing: 
                    spatial indices
                    lat/lon
                    satellite id's
            4) interval {string}: "daily" or "monthly". Monthly will gather average values over the same month.
            5) coordinates of flux tower given in [lon,lat] format. (e.g: [-100.534, 50.371])
        Output:
            1) lonData: array of longitude converted into metres from flux tower
            2) latData: array of latitude converted into metres from flux tower
            3) spatialData: array of averaged spatial index data
    """
    from lon_to_m import lon_to_m # Function to turn longitude degrees into metres
    from lat_to_m import lat_to_m # Function to turn latitude degrees into metres
    import numpy as np

    available_indices = ["NDVI", "NDWI","MNDWI_SW1","MNDWI_SW2"]
    lonData, latData, spatialData = [], [], []
    
    id = dataStruct['id']
    lon = dataStruct['longitude']
    lat = dataStruct['latitude']

    full_month = {'lonData':[],'latData':[],'spatialData':[]}

    if interval == "daily":
        for i in range(len(id)):
            if id[0][:4]=='LC08': # Checking if satellite data is Landsat
                if date == int(id[i][12:]):

                    # Appending longitude and latitude data         
                    lonData.append(lon_to_m(lon[i],coordinates))
                    latData.append(lat_to_m(lat[i],coordinates))

                    # Finding appropriate index data to append
                    spatialData.append(dataStruct[spatial_index][i])
            else:
                if date == int(id[i][:8]): # Sentinel ID format

                    # Appending longitude and latitude data         
                    lonData.append(lon_to_m(lon[i],coordinates))
                    latData.append(lat_to_m(lat[i],coordinates))

                    # Finding appropriate index data to append
                    spatialData.append(dataStruct[spatial_index][i])
    elif interval == "monthly":
        # Getting Spatial data
        monthly_ids = []
        
        for each_id in id:
            if str(date)[:6] == each_id[12:18]:
                monthly_ids.append(each_id)

        for this_month in monthly_ids:
            holding_spatialData = []
            for i in range(len(id)):
                if this_month[12:] == id[i][12]:
                    holding_spatialData.append(dataStruct[spatial_index][i])
            full_month['spatialData'].append(holding_spatialData)


        for j in range(len(full_month['spatialData'][0])): # Iterating through each point within each month (~1560)
            averaging = []
            for jj in range(len(full_month['spatialData'])): # iterating through each stored month (~4)
            
                averaging.append(full_month['spatialData'][jj][j])
            spatialData.append(np.nanmean(averaging))

        # Getting lat/lon
        if date == int(id[i][12:]):
                
                # Appending longitude and latitude data         
                lonData.append(lon_to_m(lon[i]))
                latData.append(lat_to_m(lat[i]))


            
    return np.array(lonData), np.array(latData), np.array(spatialData)
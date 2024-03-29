def landsat_footprint(longitude,latitude,spatial, ffp):
    import numpy as np
    """
    Filters arrays to only produce spatial index data that fall within flux tower footprint
        Input:
            1, 2, 3) daily satellite data for longitude, latitude, and spatial index
            4) A dict holding flux footprint arrays for ffp x values, y values, and flux values
        Output:
            A dict holding the filtered spatial data for lon, lat, and spatial index
    """
    xr = ffp['xr']
    yr = ffp['yr']
    fr = ffp['ch4']
    
    filteredData = {'lonData':[], 'latData':[],'spatialData':[]}
    
    N = len(fr)
    M = len(fr[0])
    holding_x = np.ones((N,M))*np.nan
    holding_y = np.ones((N,M))*np.nan
    
    # Finding x and y values that define the flux footprint, giving them numbers, while rest are NaN.
    for i in range(N):
        inside_ffp = np.where(~np.isnan(fr[i]))[0]
        for valid in inside_ffp:
            holding_x[i][valid] = xr[i][valid]
            holding_y[i][valid] = yr[i][valid]
    """
    - Determining for each lat and lon, whether the satellite data falls within footprint.
    - Will comb through each latitude and find points within min and max longitudes. 
    - Will look for "breaks" at given latitude where the footprint "peninsulas" into view and defines 
      localized min/max
    - Combs latitude from top to bottom.
    
    lat = satellite y-axis
    horizontal = footprint y-axis
    """
    # Reversing order of footprint x-axis to index from neg -> pos
    reversed_xr = ffp['yr'][0].iloc[::-1].reset_index(drop=True)
        
    for this_lat in np.unique(latitude)[::-1]: # [::-1] flips lat array to go from top to bottom
        
        # defining pixel edges according to landsat's 30m/px resolution
        upper_edge = this_lat + 15
        lower_edge = this_lat - 15
        
        # finding footprint horizontal slice that meets given latitude.
        for j in range(101):
            
            footprint_y = ffp['yr'][0][j]
            
            if footprint_y < upper_edge and footprint_y > lower_edge:

                # Isolating a horizontal slice as var: Slice
                Slice = []    
                breaks = []
                for ii in range(101):  
                    Slice.append(ffp['ch4'][ii][j])
                            
                # Finding breaks in NaN's, or islands of footprint data
                for iii in range(100):
                
                    # Start of an island
                    if np.isnan(Slice[iii]) and ~np.isnan(Slice[iii+1]) or ~np.isnan(Slice[iii]) and np.isnan(Slice[iii+1]):
                        breaks.append(reversed_xr[iii+1])
                        
                        
                
                if len(breaks) == 2: # 1 island of data in sea of NaN
                    for jj in range(len(longitude)):
                        if latitude[jj] == this_lat and longitude[jj] > breaks[0] and longitude[jj] < breaks[1]:
                            
                            filteredData['lonData'].append(longitude[jj])
                            filteredData['latData'].append(this_lat)
                            filteredData['spatialData'].append(spatial[jj])
                            
                elif len(breaks)== 4: # 2 islands of data in sea of NaN
                    for jj in range(len(longitude)):
                        if latitude[jj] == this_lat and longitude[jj] > breaks[0] and longitude[jj] < breaks[1] \
                            or latitude[jj] == this_lat and longitude[jj] > breaks[2] and longitude[jj] < breaks[3]:
                            
                            filteredData['lonData'].append(longitude[jj])
                            filteredData['latData'].append(this_lat)
                            filteredData['spatialData'].append(spatial[jj])
                
                
        
        
    print(f'returns {filteredData.keys()}')
    return filteredData


# ---------------------------------------------------------------------------------------------------------

def ffp_matched_to_landsat(landsat,ffp):
    """
    Averages flux hotspot values within a 30 square metre bin pertaining to each landsat pixel.
    
    Input: 
        1) Landsat dict with lat,lon, and spatial indices that are filtered through landsat_footprint function
        2) Flux footprint output with xr, yr, co2, ch4, and h fluxes
    Output:
        1) Dictionary holding xr, yr, and the three co2, ch4, and h fluxes
    """
    import numpy as np

    # List to hold the footprint values matched to the satellite coordinates
    matched_ffp = {'xr':[],'yr':[],'co2':[],'ch4':[],'h':[]}

    # Blacking out ffp xr and yr that our outside of footprint (original = xr,yr are full and fr is NaN'd out)
    N = len(ffp['co2'])
    M = len(ffp['co2'][0])
    holding_x = np.ones((N,M))*np.nan
    holding_y = np.ones((N,M))*np.nan

    # Finding x and y values that define the flux footprint, giving them numbers, while rest are NaN.
    for i in range(N):
        inside_ffp = np.where(~np.isnan(ffp['co2'][i]))[0]
        for valid in inside_ffp:
            holding_x[i][valid] = ffp['xr'][i][valid]
            holding_y[i][valid] = ffp['yr'][i][valid]
            

    for i in range(len(landsat['lonData'])):
        # Variable that holds each pixel's: [0] left bound, [1]right bound, [2] upper bound, [3] lower bound
        pixel = []
        pixel.append(landsat['lonData'][i] - 15)
        pixel.append(landsat['lonData'][i] + 15)
        pixel.append(landsat['latData'][i] + 15)
        pixel.append(landsat['latData'][i] - 15)
        
        ffp_bin = {'xr':[],'yr':[],'co2':[],'ch4':[],'h':[]} # List holding all the ffp points that falls within satellite pixel
        
        for j in range(101):
            for j2 in range(101):
                if ~np.isnan(holding_x[j][j2]) and ~np.isnan(holding_y[j][j2]):
                    ffp_xr = ffp['xr'][j][j2]
                    ffp_yr = ffp['yr'][j][j2]
                    
                    if ffp_xr > pixel[0] and ffp_xr < pixel[1] and  ffp_yr < pixel[2] and ffp_yr > pixel[3]:
                        
                        ffp_bin['co2'].append(ffp['co2'][j][j2])
                        ffp_bin['ch4'].append(ffp['ch4'][j][j2])
                        ffp_bin['h'].append(ffp['h'][j][j2])
                        ffp_bin['xr'].append(ffp_xr)
                        ffp_bin['yr'].append(ffp_yr)
                        
        if i % 100 == 0:
            print(f'progress: {i}/{len(landsat["lonData"])}')
                
        matched_ffp['co2'].append(np.nanmean(ffp_bin['co2']))
        matched_ffp['ch4'].append(np.nanmean(ffp_bin['ch4']))
        matched_ffp['h'].append(np.nanmean(ffp_bin['h']))
        matched_ffp['xr'].append(np.nanmean(ffp_bin['xr']))
        matched_ffp['yr'].append(np.nanmean(ffp_bin['yr']))

    return matched_ffp
        
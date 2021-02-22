def sector_plot(date, ffp_filename):
    """
    This script overlays Landsat 8 data on top of relative flux data from Camilo Rey-Sanchez's methane 
    hotspot model (FFP)to generate statistical correlations between remote sensing indices and methane 
    emissions.
    
    Remote sensing indices used in this analysis are:
        1) NDVI - Vegetation greenery
        2) NDWI - Surface water index
        3) MNDWI - Leaf water content
            > MNDWI uses landsat 8's B6 band as SWIR (1.566-1.651 μm)
            > MNDWI2 uses landsat 8's B7 band as SWIR (2.107-2.294 μm)
        4) Brightness temperature
    
    Note:
    Available Landsat 8 dates (yyyy/mm/dd) for this script's "date" input are:

    20130328 20130514 20130615 20130710 20130717 20130726 20130912 20131014
    20131122 20131208 20140125 20140203 20140219 20140602 20140713 20140729
    20140821 20140906 20140915 20150222 20150326 20150411 20150520 20150529
    20150605 20150614 20150621 20150630 20150723 20150801 20150817 20150909
    20151004 20151121 20151128 20151230 20160124 20160209 20160225 20160312
    20160404 20160420 20160429 20160506 20160607 20160718 20160725 20160819
    20160911 20160920 20160927 20170110 20170202 20170525 20170626 20170705
    20170712 20170728 20170822 20170829 20170914 20170923 20171009 20180309
    20180325 20180426 20180505 20180512 20180715 20180724 20180731 20180809
    20180816 20180917 20180926 20181019 20181028 20181206 20190107 20190217
    20190321 20190328 20190429 20190508 20190515 20190531 20190616 20190803
    20190819 20190828 20190904 20190929 20191022 20191031 20200126 20200220
    20200415 20200510 20200526 20200618 20200720 20200729
    
    Note:
    Camilo output files have to have this naming convention: BB_fluxMap_x_june_aug2017
    Can change expected filenames on lines: 82-86.

    Inputs: 
        date {int} = Landsat image date. (e.g.: 20180523)
        ffp_filename {string} = Suffix of Camilo output files (e.g. 'may2018.csv')
    Returns:
        4 figures
            fig: discretized flux footprint map with sector overlay
            fig2: Correlation with sector-binned landsat vs. ffp
            fig3: Flux footprint visualization
            fig4: Unbinned spatial correlation landsat vs. ffp

    Display figures with:

    >from IPython.display import display
    >display(fig,fig2,fig3,fig4)

    """
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from get_spatial import get_spatial
    from scipy import stats
    import os

    # Importing Landsat 8 data. Original data gathered from Google Earth Engine
    data = pd.read_csv('bb1_spatial_indices_big.csv',delimiter = ',',header = 1)

    # List of remote sensing indices to be used in this analysis
    indices = ['MNDWI2','MNDWI','NDWI','NDVI','temp']

    # Landsat ID suffix corresponding to analysis date. Refer to script description for list of dates.
    ANALYSIS_DATE = date

    # Getting Landsat data for specified date from sub function: get_spatial.py
    spatialData = {'MNDWI2':[],'MNDWI':[],'NDVI':[],'NDWI':[],'temp':[]}
    lonData, latData, spatialData['MNDWI2'] = get_spatial(ANALYSIS_DATE, 'MNDWI_SW2',data,'daily')
    lonData, latData, spatialData['NDVI'] = get_spatial(ANALYSIS_DATE, 'NDVI',data,'daily')
    lonData, latData, spatialData['NDWI'] = get_spatial(ANALYSIS_DATE, 'NDWI',data,'daily')
    lonData, latData, spatialData['MNDWI'] = get_spatial(ANALYSIS_DATE, 'MNDWI_SW1',data,'daily')
    lonData, latData, spatialData['temp'] = get_spatial(ANALYSIS_DATE, 'CELSIUS',data,'daily')

    # FFP datafile name created from Camilo Rey-Sanchez's matlab model. 
    newFileName = ffp_filename # FFP filename from script input.

    # fluxmap outputs from Camilo's are saved in "data" subfolder
    os.chdir('data')
    ffp = {}
    ffp['xr'] = pd.read_csv('BB_fluxMap_x_'+newFileName,header = -1) # x-coordinates
    ffp['yr'] = pd.read_csv('BB_fluxMap_y_'+newFileName,header = -1) # y-coordinates
    ffp['co2'] = pd.read_csv('BB_fluxMap_co2_'+newFileName,header = -1) # CO2 spatial data
    ffp['ch4'] = pd.read_csv('BB_fluxMap_ch4_'+newFileName,header = -1) # CH4 spatial data
    ffp['h'] = pd.read_csv('BB_fluxMap_h_'+newFileName,header = -1) # Sensible heat spatial data
    os.chdir('..')
    # cd ../

    # Importing sub-function that cuts out the landsat pixels found in the flux footprint area
    from landsat_footprint import landsat_footprint
    # Storing landsat data in dict called landsat
    landsat = {'MNDWI2':[],'MNDWI':[],'NDVI':[],'NDWI':[],'temp':[],'lonData':[],'latData':[]}

    # Each iteration of landsat_footprint sub-function deals with only 1 spatial index. Do this for each index of interest
    sat = landsat_footprint(lonData,latData,spatialData['MNDWI2'], ffp)
    landsat['MNDWI2'] = sat['spatialData']
    sat = landsat_footprint(lonData,latData,spatialData['MNDWI'], ffp)
    landsat['MNDWI'] = sat['spatialData']
    sat = landsat_footprint(lonData,latData,spatialData['NDWI'], ffp)
    landsat['NDWI'] = sat['spatialData']
    sat = landsat_footprint(lonData,latData,spatialData['NDVI'], ffp)
    landsat['NDVI'] = sat['spatialData']
    sat = landsat_footprint(lonData,latData,spatialData['temp'], ffp)
    landsat['temp'] = sat['spatialData']
    landsat['lonData'] = sat['lonData']
    landsat['latData'] = sat['latData']

    #Matching FFP resolution to landsat resolution
    from landsat_footprint import ffp_matched_to_landsat
    # Camilo's hotspot data has finer spatial resolution than landsat's 30 square metre resolution.
    # This sub-function creates average hotspot values within each 30 square metre area. End result is
    # a spatial map of methane/co2/H hotspot data corresponding to each landsat pixel (essentially matching
    # dataset lengths).
    matched_ffp = ffp_matched_to_landsat(landsat,ffp) # dict keys are the same for "matched_ffp" as for "landsat"

    # ----------------------------------RADIAL PLOT (fig)------------------------------------------------------------
    """
    Categorizing datapoints by radial bins. Spatial map will be split into 8 sectors separated by
    45˚. Each point's sector will be determined by a vector projection method to see how it falls
    within the two walls of a sector (side 1 and side 2). If the angle between the ffp vector and a 
    sector's two sides were less than 45˚, the ffp data point would be binned.
    """
    
    theta = 0 # starting angle of first sector

    first = max(matched_ffp['xr'])+60 # This is max distance of a datapoint + some. Used to plot sector walls on figure.
    u = np.array([0,0]) # Shell to hold ffp point's vector coordinates [x,y]
    v1 = np.array([0,0]) # Shell to hold sector's side 1 coordinates
    v2 = np.array([0,0]) # Shell to hold sector's side 2 coordinates

    # Plotting radial grid template

    fig = plt.figure(figsize = (5,3.5)) # RADIAL BINNING PLOT figure

    # Plotting just the walls of each radial sector.
    for i in range(8):
        diagonal_x = first*np.cos(theta)
        diagonal_y = -first*np.sin(theta)
        plt.plot([0,diagonal_x],[0,diagonal_y],'--k',alpha = 0.5)

        theta += np.pi/4
        diagonal_x = first*np.cos(theta)
        diagonal_y = -first*np.sin(theta)
        plt.plot([0,diagonal_x],[0,diagonal_y],'--k',alpha = 0.5)

    # Plotting hotspot datapoints
    plt.scatter(matched_ffp['xr'],matched_ffp['yr'],c=matched_ffp['ch4'])



    # EMPTY Bin list for each sector. 8 sectors total, each list contains points for 1 sector. "sector_x"
    # is all the x-coordinates, "sector_y" is all the y-coordinates.
    sector_x = [[],[],[],[],[],[],[],[]]
    sector_y = [[],[],[],[],[],[],[],[]]
    sector_ffp = [[],[],[],[],[],[],[],[]]
    sector_landsat = {'NDVI': [[],[],[],[],[],[],[],[]],
                    'NDWI':[[],[],[],[],[],[],[],[]],
                    'MNDWI':[[],[],[],[],[],[],[],[]],
                    'temp':[[],[],[],[],[],[],[],[]],
                    'MNDWI2':[[],[],[],[],[],[],[],[]]}

    # Turning the bin lists into empty lists
    for i in range(8):
        sector_x[i].clear()
        sector_y[i].clear()
        sector_ffp[i].clear()

    for sect in range(8):
        # sector SIDE 1 vector
        v1[0] = first*np.cos(theta) # x
        v1[1] = -first*np.sin(theta) # y

        theta += np.pi/4
        
        # sector SIDE 2 vector
        v2[0] = first*np.cos(theta) # x
        v2[1] = -first*np.sin(theta) # y
        
        
        for i in range(len(matched_ffp['xr'])):
        #   x-coordinate (ffp)
            u[0] = matched_ffp['xr'][i]
        #   y-coordinate (ffp)
            u[1] = matched_ffp['yr'][i]

            # Vector projection on sector SIDE 1: proj = (u dot v)/|v|2 * v
            dot1 = u[0]*v1[0] + u[1]*v1[1]
            vMag1 = (np.sqrt(v1[0]**2+v1[1]**2))**2
            proj1 = (dot1/vMag1) * v1


            # Checking ffp-vector angle from sector SIDE 1. Keep if theta < or = pi/4
            len_proj = np.sqrt(proj1[0]**2+proj1[1]**2)
            len_vector = np.sqrt(u[0]**2 + u[1]**2)
            check = len_proj/len_vector
            check_theta1 = np.arccos(check)

            # -------- vvv SIDE 2: Looking for points between side 1 and side 2 vvv -----------
            

            # Vector projection on sector SIDE 2: proj = (u dot v)/|v|2 * v
            dot2 = u[0]*v2[0] + u[1]*v2[1]
            vMag2 = (np.sqrt(v2[0]**2+v2[1]**2))**2
            proj2 = (dot2/vMag2) * v2

            # Checking ffp-vector angle from sector SIDE 2. Keep if it's within theta = pi/4
            len_proj = np.sqrt(proj2[0]**2+proj2[1]**2)
            len_vector = np.sqrt(u[0]**2 + u[1]**2)
            check = len_proj/len_vector
            check_theta2 = np.arccos(check)

            # dot > 0 condition is to filter for projections over 90˚
            if dot1 > 0 and dot2>0 and check_theta1 <= np.pi/4 and check_theta2 <= np.pi/4:
                # Storing each sector's ffp data
                sector_x[sect].append(matched_ffp['xr'][i])
                sector_y[sect].append(matched_ffp['yr'][i])
                sector_ffp[sect].append(matched_ffp['ch4'][i])

                # Storing each sector's landsat data
                for index in indices:
                    sector_landsat[index][sect].append(landsat[index][i])
    
    # ------------------------------------ CORRELATION (fig2) ------------------------------------------------
    # Getting average values within each sector
    sector_ffp_average = []
    sector_landsat_average = {'MNDWI2':[],'MNDWI':[],'NDVI':[],'NDWI':[],'temp':[]}
    for sect in range(8):
        if np.nanmean(sector_ffp[sect]) < 1000: # Skipping nan values (for stat purposes)
            sector_ffp_average.append(np.nanmean(sector_ffp[sect]))
        for index in indices:
            if np.nanmean(sector_landsat[index][sect]) < 1000: # Skipping nan values (for stat purposes)
                sector_landsat_average[index].append(np.nanmean(sector_landsat[index][sect]))

    fig2, ax = plt.subplots(1,5,figsize = (35,5))
    plot = 0 # subplot figure indexing
    for index in indices:

        ax[plot].scatter(sector_landsat_average[index],sector_ffp_average)
        
    #     Regression
        m, b = np.polyfit(sector_landsat_average[index],sector_ffp_average,1)
        yfit = m*np.array(sector_landsat_average[index])+b
        ax[plot].plot(sector_landsat_average[index],yfit,'orange')
        
        r_val, p_val = stats.pearsonr(sector_landsat_average[index],sector_ffp_average)
        corr = f'{index}\n \n r = {np.round(r_val,3)} \np = {np.round(p_val,3)}'
        
    #     Formatting Plot
        ax[plot].set_title(index,fontsize = 24)
        ax[plot].set_xlabel(corr, fontsize = 16, labelpad = 20)
        ax[plot].set_ylabel(r'Methane Flux [$µmol/m^2s$]', fontsize = 16)
        
        plot +=1

    # ------------------------------------Non-Binned Comparison ------------------------------------------------
    # NON SECTOR-BINNED PLOT

    # Raw flux maps
    fig3, ax2 = plt.subplots(1,3,figsize = (20,5))
    ax2[0].scatter(landsat['lonData'],landsat['latData'],c=landsat['MNDWI2'],marker='s',cmap = 'magma', s = 700)
    ax2[1].scatter(matched_ffp['xr'],matched_ffp['yr'],c=matched_ffp['ch4'], cmap = 'magma', s = 700)
    ax2[2].pcolormesh(ffp['xr'],ffp['yr'],ffp['ch4'],cmap='magma')

    ax2[0].set_title('Landsat Spatial Index')
    ax2[1].set_title('Binned K&M Flux Footprint')
    ax2[2].set_title('Raw K&M Flux Footprint')
    ax2[0].set_xlim([-100,150]), ax2[1].set_xlim([-100,150]), ax2[2].set_xlim([-100,150])
    ax2[0].set_ylim([-150,60]), ax2[1].set_ylim([-150,60]), ax2[2].set_ylim([-150,60])

    # Non sector-binned correlation plotting
    fig4, ax3 = plt.subplots(1,5,figsize = (35,5))
    indices = ['MNDWI2','MNDWI','NDWI','NDVI','temp']
    plot = 0
    for idx in indices:
        ax3[plot].scatter(landsat[idx],matched_ffp['ch4'])
        
        
        
    #     Regression
        m, b = np.polyfit(landsat[idx],matched_ffp['ch4'],1)
        yfit = m*np.array(landsat[idx])+b
        ax3[plot].plot(landsat[idx],yfit,'orange')
        
        r_val, p_val = stats.pearsonr(landsat[idx],matched_ffp['ch4'])
        corr = f'{idx}\n \n r = {np.round(r_val,3)} \np = {np.round(p_val,10)}'
        
    #     Plot formatting
        ax3[plot].set_title(idx,fontsize = 24)
        ax3[plot].set_xlabel(corr, fontsize = 16,labelpad = 20)
        ax3[plot].set_ylabel(r'Methane Flux [$µmol/m^2s$]', fontsize = 16)
        
        plot +=1
        
    fig4.subplots_adjust(hspace = 0.4)

    return fig, fig2, fig3, fig4
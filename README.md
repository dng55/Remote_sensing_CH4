# Remote_sensing_CH4
Combining remote sensing products from Google Earth Engine with a methane emission model to characterize surface conditions of methane hotspots in wetlands. 

This method relies on 2D spatial outputs from Camilo-Rey Sanchez's Footprint Aggregated Relative Flux Mapping model. Landsat 8 maps are then overlaid to analyze the correlation between satellite spatial indices (NDVI, NDWI, Brightness Temp) and methane emissions.
----------------------------------------------------------

Scripts:
1) sector_plot.py
    - sector_plot.py is the final python script that holds all sub-functions that work together to organize Landsat 8 and FARF data for the purposes of this analysis. Read comments for function input details. A broad overview:

      1) Reads Landsat 8 spatial index data exported as a .csv from Google Earth Engine.
        2) Grabs single Landsat date from full satellite image dataset that ranges from 03/2013 - 07/2020.
        3) Reads methane hotspot model data from Camilo-Rey Sanchez's model
        4) Uses Flux Footprint modelling (K&M) to mask out landsat data that's not within 80% of flux tower's footprint.
        5) Bins hotspot data into 30 sq.m cells to match Landsat 8's spatial resolution (Hotspot model has a much finer resolution than Landsat).
        6) We now have a preliminary pair of maps (one Landsat, one hotspot 2D model) to compare between. sector_plot.py does a preliminary correlation analysis to show the relationship between spatial indices (NDVI, NDWI, BT) and CH4 emissions
        7) To account for artifacts in hotspot model (hotspots cast "shadows"  of higher emissions that trail out from the origin), both maps have their data binned into radial cells that expand out from the origin at an angle pi/4 (i.e. map is divided up like pizza slices). 
        8) Final correlation analysis is done with these sectored maps to study the relationship between spatial indices and CH4 emissions.
    
    - Generates 4 figures: 
          - fig: Discretized flux footprint map with bin sector overlay (after step e, and outlines from step g overlaid)
          - fig2: Correlation with sector-binned landsat vs. ffp (step h)
          - fig3: Flux footprint visualization (step e)
          - fig4: Unbinned spatial correlation landsat vs. ffp (step f)
        
    - Example of how to call script and show figures in Jupyter Notebooks:
          - from sector_plot import sector_plot
          - from IPython.display import display
          - fig,fig2,fig3,fig4 = sector_plot(20170728, 'june_aug2017.csv')
          - display(fig,fig2,fig3,fig4)
    
2) get_spatial.py
    - get_spatial.py is a sub-function that gathers a single landsat image of a specified date. Outputs: 1) latitude, 2) longitude, 3) spatial index

3) landsat_footprint.py
    - landsat_footprint.py holds 2 sub-functions: landsat_footprint, and ffp_matched_to_landsat
        - landsat_footprint: masks out all satellite data that falls outside of the flux footprint. 

        - ffp_matched_to_landsat: bins hotspot model into 30 sq.m cells to match landsat spatial resolution

4) lat_to_m.py and lon_to_m.py
    - lat_to_m and lon_to_m are sub-functions to turn latitude and longitude degrees into metres.

5) v1_Landsat_Spatial.js
    - Javascript code for Google Earth Engine to collect spatial index data from a specified region, and filters for snow and cloud coverage. Outputs as csv file containing NDVI, NDWI, MNDWI, BT, Lat, Lon
    - Access this code in my Google Earth Engine repo at: https://code.earthengine.google.com/?scriptPath=users%2FDNG%2Fgee_code%3A1v%20Final%20Spatial%20Indices

6) Landsat_LST.js
    - Edited Javascript code (original from Sofia Ermida) that computes NDVI, NDWI, MNDWI, and BT



Data:
- Keep landsat data in same folder as python scripts, but hotspot files are in a sub-folder called "data"

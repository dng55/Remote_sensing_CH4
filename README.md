# Remote_sensing_CH4
Combining remote sensing products from Google Earth Engine with a methane emission model to characterize surface conditions of methane hotspots in wetlands. 

This method relies on 2D spatial outputs from Camilo-Rey Sanchez's Footprint Aggregated Relative Flux Mapping model. Landsat 8 maps are then overlaid to analyze the correlation between satellite spatial indices (NDVI, NDWI, Brightness Temp) and methane emissions.
----------------------------------------------------------

Scripts:
- sector_plot.py
  - sector_plot.py is the final python script that holds all sub-functions that work together to organize Landsat 8 and FARF data for the purposes of this analysis. A broad overview:

     1) Reads Landsat 8 spatial index data exported as a .csv from Google Earth Engine.
    2) Grabs single Landsat date from full satellite image dataset that ranges from 03/2013 - 07/2020.
    3) Reads methane hotspot model data from Camilo-Rey Sanchez's model
    4) Uses Flux Footprint modelling (K&M) to mask out landsat data that's not within 80% of flux tower's footprint.
    5) Bins hotspot data into 30 sq.m cells to match Landsat 8's spatial resolution (Hotspot model has a much finer resolution than Landsat).
    6) We now have a preliminary pair of maps (one Landsat, one hotspot 2D model) to compare between. sector_plot.py does a preliminary correlation analysis to show the relationship between spatial indices (NDVI, NDWI, BT) and CH4 emissions
    7) To account for artifacts in hotspot model (hotspots cast "shadows"  of higher emissions that trail out from the origin), both maps have their data binned into radial cells that expand out from the origin at an angle pi/4 (i.e. map is divided up like pizza slices). 
    8) Final correlation analysis is done with these sectored maps to study the relationship between spatial indices and CH4 emissions.
    
  - Generates 4 figures: 
        fig: Discretized flux footprint map with bin sector overlay (after step 5, and outlines from step 7 overlaid)
        fig2: Correlation with sector-binned landsat vs. ffp (step 8)
        fig3: Flux footprint visualization (step 5)
        fig4: Unbinned spatial correlation landsat vs. ffp (step 6)
        
  - Example of how to call script and show figures in Jupyter Notebooks:
      from sector_plot import sector_plot
      from IPython.display import display
      fig,fig2,fig3,fig4 = sector_plot(20170728, 'june_aug2017.csv')
      display(fig,fig2,fig3,fig4)
    
      

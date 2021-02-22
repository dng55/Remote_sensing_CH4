% Fast Camilo Plotting

clear all;
% FP_Opts_BB
cd '/Users/darianng/Documents/YEAR 4/Directed Studies/Footprint_Code/Footprints-master/CalculateFootprint/Run_options'

% tstart = '2018-08-213 00:00';
% tend = '2018-08-243 24:00';
tstart = '2017-06-152 00:00';
tend = '2017-08-243 24:00';

FP_opts_BB;

% Footprint_Run_Continuous
cd '/Users/darianng/Documents/YEAR 4/Directed Studies/Footprint_Code/Footprints-master/CalculateFootprint'
Footprint_Run_Continuous;
% Surface_Flux_Map
cd '/Users/darianng/Documents/YEAR 4/Directed Studies/Footprint_Code/Footprints-master/Analyze_Outputs'
Surface_Flux_Map;
// -- Setup: imports and.. -- 
// Dates of interest
var start = ee.Date('2010-01-01');
var end = ee.Date('2021-01-05');

// analysis area
var roi = Areabb2;



// Loading image library
var landsat_sr = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
  .filterBounds(bb1) // Include only region of interest
  .filterDate(start,end) // Include only dates of interest
  .sort('system:time_start');


// Getting individual lat and lon from Geometry
var lon = bb1.coordinates().get(0).getInfo();
var lat = bb1.coordinates().get(1).getInfo();

// Center map over region of interest
Map.setCenter(lon,lat,12);


// Sofia LST.js
// link to the code that computes the Landsat LST
// var LandsatLST = require('users/sofiaermida/landsat_smw_lst:modules/Landsat_LST.js')
var LandsatLST = require('users/DNG/gee_code:modules/Landsat_LST.js')


// select region of interest, date range, and landsat satellite
var geometry = roi;
var satellite = 'L8';
var use_ndvi = true;

// get landsat collection with added variables: NDVI, FVC, TPW, EM, LST
var LandsatColl = LandsatLST.collection(satellite, start, end, geometry, use_ndvi)
print('Sofia landsat collection:',LandsatColl)

var exImage = LandsatColl.first();



// Converting Kelvin to Celsius
function K_to_C(image) {
  var celsius = image.select('LST').subtract(273.15).rename('CELSIUS')
  return image.addBands(celsius);
}

// Mapping Conversion to collection
var celsiusCollection = LandsatColl.map(K_to_C)
print(celsiusCollection)



// ------vvv----- CLOUD FILTERING -----vvv-------//

var landsat_toa = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')
  .filterBounds(bb1) // Include only region of interest
  .filterDate(start,end) // Include only dates of interest
  .sort('system:time_start');

// Function to map landsat cloud filtering algorithm onto an image collection 
function cloudFilter(imageCollection) {
  return imageCollection.map(function(image){
    var cloud = ee.Algorithms.Landsat.simpleCloudScore(image).select('cloud');
    var cloudiness = cloud.reduceRegion({
      reducer: 'mean',
      geometry: roi,
      scale: 30,
    });
    return image.set(cloudiness) // Saves cloudiness over region as property: 'cloud'
  })
}

// Filtering by 'cloud' value
var cloudlessLandsat = cloudFilter(landsat_toa).filter(ee.Filter.lte('cloud',10));
print('filter by roi is: ',cloudlessLandsat);



// ------^^^----- CLOUD FILTERING -----^^^-------//



// Create an NDVI time-series for BurnsBog 1.
function MakeChart(imgCollection,location){
  return ui.Chart.image.series({
    imageCollection: imgCollection.select('NDVI'),
    region: location,
    reducer: ee.Reducer.first(),
    scale: 30
  }).setOptions({title: 'NDVI Timeseries'});
}
// var bb1chart = MakeChart(CollectionNDVI,bb1);
// print('Cloud-filtered NDVI time series',bb1chart);


// // Comparing to unfiltered imagecollection
// var originalNDVI = landsat_toa.map(addNDVI);
// var unfiltered = MakeChart(originalNDVI,bb1);
// print('unfiltered NDVI time series',unfiltered);



// print(keyboard);



// --------- Masking Operations to Landsat_SR (Atmosphere adjusted) --------------//




// Gathering list of clear-sky dates from filtered TOA imageCollection
var collectionDates = cloudlessLandsat
    .map(function(image) {
      var milli = image.get('system:time_start'); // Getting milliseconds property
      var ymd = ee.Date(milli).format('YYYY-MM-dd'); // Converting ms to yyyy-mm-dd
      return ee.Feature(null, {'date': ymd});
    })
    .distinct('date') // Finding distinct dates in case there are duplicates
    .aggregate_array('date'); // Aggregating as list
  
print('List of dates',collectionDates);



// print(keyboard)


// Creating new image property: Time in yyyy-mm-dd format
function getYMD(colln){
  return colln.map(function(image){
    var d = image.get('system:time_start');
    var ymd = ee.Date(d).format('YYYY-MM-dd');
    return image.set({'YMD_Date': ymd});
  });
}

// Giving each image in SR imageCollection its yyyy-mm-dd property
var celsius_YMD = getYMD(celsiusCollection);

// Gathering all the clear-sky images in the SR collection
var finalCollection = celsius_YMD.filter(ee.Filter.inList("YMD_Date", collectionDates));
print('Final landsat collection',finalCollection);



// print(keyboard)


// // Creating atmosphere adjusted time series
// var chart_SR = MakeChart(finalCollection,bb1)
// print('Atmosphere corrected temperature',chart_SR)



// var testing = celsius_YMD.filterMetadata('YMD_Date','equals','2018-03-09')
// print('testing image is:',testing.first())

// Map.addLayer(testing.first().select('LST'),{min:270, max:283, palette:cmap1},'testing image')




// // Making Animation
// var col = filtered_SR.select('NDVI')

// var gifRegion = roi

// // Create RGB visualization images for use as animation frames.
// var rgbVis = col.map(function(img) {
//   return img.visualize(vizParams).clip(gifRegion);
// });

// var gifParams = {
//   'region': gifRegion,
//   'dimensions': 600,
//   'crs': 'EPSG:3857',
//   'framesPerSecond': 10
// };
// var gifStyle = {
//   'border': '10px solid black'
// };

// print(ui.Thumbnail(rgbVis, gifParams,gifStyle));

var output_variables = ee.List(['CELSIUS','NDVI','NDWI','MNDWI_SW1','MNDWI_SW2'])


// Exporting 2d NDVI data
var justCelsius = finalCollection.select(output_variables); // Getting only ndvi band

var output = justCelsius.getRegion(roi, 30); // Specifying region

var output_index = output.get(0); // Printing out csv headers
print('index',output_index);


var outputFeatures = ee.FeatureCollection(output.map(function(el){
  el = ee.List(el); // cast every element of the list
  var geom = roi;
  return ee.Feature(geom, {
    'id':ee.Number(el.get(0)), 
    'longitude':ee.Number(el.get(1)),
    'latitude':ee.Number(el.get(2)),
    'time':ee.Number(el.get(3)),
    'Temperature':ee.Number(el.get(4)),
    'NDVI':ee.Number(el.get(5)),
    'NDWI':ee.Number(el.get(6)),
    'MNDWI':ee.Number(el.get(7)),
    'MNDWI2':ee.Number(el.get(8))
  });
}));


Export.table.toDrive({
  collection: outputFeatures,
  folder: 'Micromet_GEE',
  description:'bb2_spatial_indices_2021',
  fileFormat: 'CSV'
});

// var testimage = landsat_sr.filterDate(ee.Date('2017-02-01'),ee.Date('2017-02-03'))
// var test = LandsatLST.collection(satellite, ee.Date('2017-02-01'), ee.Date('2017-02-03'), geometry, use_ndvi)

// var exImage = test.first();
// var cmap1 = ['blue', 'cyan', 'green', 'yellow', 'red'];
// var cmap2 = ['F2F2F2','EFC2B3','ECB176','E9BD3A','E6E600','63C600','00A600']; 
// Map.addLayer(exImage.select('LST'),{min:290, max:320, palette:cmap1}, 'LST')

var bb1chart = MakeChart(finalCollection,bb1);
print('BB1 Cloud-filtered NDVI time series',bb1chart);

var bb2chart = MakeChart(finalCollection,bb2);
print('BB2 Cloud-filtered NDVI time series',bb2chart);
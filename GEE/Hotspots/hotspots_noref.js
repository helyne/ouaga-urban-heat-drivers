// ==========================================================
// TEMPORARY UHI HOTSPOT MAP (NO RURAL REFERENCE - FULL YEAR 2024)
// Purpose: produce binary hotspot map now while rural reference is unavailable
// Method: LST median -> Hotspot threshold = Mean + 1 * StdDev
// Data: Landsat-8 C2/T1_L2 (ST_B10) | 2024-01-01 -> 2024-12-31
// Note: UHII / rural logic is commented out below for future use.
// ==========================================================



// ==========================================================
// 1. LOAD URBAN AREA (OUAGADOUGOU)
// ==========================================================
var urban = ee.FeatureCollection("projects/hotspotters/assets/Ouaga_boundary");
Map.centerObject(urban, 11);



// ==========================================================
// 2. LOAD LANDSAT-8 IMAGES AND COMPUTE LST (°C)
// ==========================================================
var L8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
  .filterDate('2024-01-01', '2024-12-31')
  .filterBounds(urban)
  .map(function(img) {
    // QA band for cloud masking
    var qa = img.select('QA_PIXEL');

    // Convert TIRS band (ST_B10) to LST in Celsius using the L2 scaling
    var lst = img.select('ST_B10')
                 .multiply(0.00341802)   // radiance/rescaling factor
                 .add(149.0)             // radiance offset
                 .subtract(273.15)       // Kelvin -> Celsius
                 .rename('LST');

    // Cloud mask (bit 6 = cloud confidence)
    var mask = qa.bitwiseAnd(1 << 6).eq(0);

    return lst.updateMask(mask)
              .copyProperties(img, ['system:time_start']);
  });



// ==========================================================
// 3. CREATE YEARLY MEDIAN LST COMPOSITE (2024)
// ==========================================================
var LST = L8.median().clip(urban);

Map.addLayer(LST, {
  min: 20,
  max: 45,
  palette: ['blue', 'yellow', 'red']
}, 'Median LST (2024)');



// ==========================================================
// 4. COMPUTE CITY-WIDE MEAN AND STANDARD DEVIATION
//    (Used for statistical hotspot thresholding)
// ==========================================================
var stats = LST.reduceRegion({
  reducer: ee.Reducer.mean().combine({
    reducer2: ee.Reducer.stdDev(),
    sharedInputs: true
  }),
  geometry: urban,
  scale: 30,
  maxPixels: 1e13
});

var meanLST = ee.Number(stats.get('LST_mean'));
var stdLST  = ee.Number(stats.get('LST_stdDev'));

print('Mean LST (°C):', meanLST);
print('Std Dev (°C):', stdLST);



// ==========================================================
// 5. DEFINE HOTSPOT THRESHOLD = Mean + 1 * StdDev
// ==========================================================
var threshold = meanLST.add(stdLST);
print('Hotspot threshold (°C):', threshold);



// ==========================================================
// 6. EXTRACT HOTSPOTS (BINARY MAP)
//    Hotspot pixels = LST > threshold
// ==========================================================
var hotspots = LST.gt(threshold).selfMask();

Map.addLayer(hotspots, {palette: ['red']}, 'UHI Hotspots (No Rural Ref)');



// ==========================================================
// 7. EXPORT HOTSPOT MAP (GeoTIFF)
// ==========================================================
Export.image.toDrive({
  image: hotspots,
  description: 'Ouagadougou_Hotspots_2024_NoRural',
  region: urban,
  scale: 30,
  maxPixels: 1e13
});

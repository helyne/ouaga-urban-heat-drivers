{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 // ==========================================================\
// UHI HOTSPOT EXTRACTION FOR OUAGADOUGOU (2024)\
// Method: UHI Intensity (UHII)\
// Dataset: Landsat-8 TIRS Band 10\
// Period: Jan 1 \'96 Dec 31, 2024\
// Threshold: UHII > 0.2 = HOTSPOT\
// ==========================================================\
\
\
\
// ==========================================================\
// 1. LOAD URBAN AREA (OUAGADOUGOU)\
// ==========================================================\
var urban = ee.FeatureCollection("projects/hotspotters/assets/Ouaga_boundary");\
Map.centerObject(urban, 11);\
\
\
\
// ==========================================================\
// 2. LOAD RURAL REFERENCE AREA\
// (MUST NOT OVERLAP URBAN ZONE)\
// ==========================================================\
var rural = ee.FeatureCollection("projects/hotspotters/assets/Ouaga_rural");\
\
\
\
// ==========================================================\
// 3. LOAD LANDSAT-8 IMAGES AND COMPUTE LST (\'b0C)\
// ==========================================================\
var L8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")\
  .filterDate('2024-01-01', '2024-12-31')\
  .filterBounds(urban)\
  .map(function(img) \{\
\
    // Extract QA band for cloud masking\
    var qa = img.select('QA_PIXEL');\
\
    // Convert Band 10 to Land Surface Temperature (\'b0C)\
    var lst = img.select('ST_B10')\
                 .multiply(0.00341802)\
                 .add(149.0)\
                 .subtract(273.15)\
                 .rename('LST');\
\
    // Remove cloudy pixels\
    var mask = qa.bitwiseAnd(1 << 6).eq(0);\
\
    return lst.updateMask(mask)\
              .copyProperties(img, ['system:time_start']);\
  \});\
\
\
\
// ==========================================================\
// 4. YEARLY MEDIAN LST MAP\
// ==========================================================\
var LST = L8.median().clip(urban);\
\
Map.addLayer(LST, \{\
  min: 20,\
  max: 45,\
  palette: ['blue', 'yellow', 'red']\
\}, 'Median LST 2024');\
\
\
\
// ==========================================================\
// 5. COMPUTE RURAL REFERENCE TEMPERATURE (TR)\
// ==========================================================\
var TR = ee.Number(\
  LST.reduceRegion(\{\
    reducer: ee.Reducer.mean(),\
    geometry: rural,\
    scale: 30,\
    maxPixels: 1e13\
  \}).get('LST')\
);\
\
print('Rural reference temperature TR (\'b0C):', TR);\
\
\
\
// ==========================================================\
// 6. COMPUTE UHII MAP\
// ==========================================================\
var UHII = LST.subtract(TR)\
              .divide(TR)\
              .rename('UHII');\
\
Map.addLayer(UHII, \{\
  min: -0.1,\
  max: 0.5,\
  palette: ['blue', 'cyan', 'yellow', 'red']\
\}, 'UHII 2024');\
\
\
\
// ==========================================================\
// 7. DEFINE HOTSPOTS (UHII > 0.2)\
// ==========================================================\
var hotspots = UHII.gt(0.2).selfMask();\
\
Map.addLayer(hotspots, \{\
  palette: ['red']\
\}, 'UHI Hotspots 2024');\
\
\
\
// ==========================================================\
// 8. EXPORT HOTSPOT MAP\
// ==========================================================\
Export.image.toDrive(\{\
  image: hotspots,\
  description: 'Ouagadougou_UHI_Hotspots_2024',\
  region: urban,\
  scale: 30,\
  maxPixels: 1e13\
\});\
}
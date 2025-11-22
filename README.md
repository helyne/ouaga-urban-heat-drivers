# Cross-City Insights into Urban Heat Hot-spots: Evidence from Ouagadougou, Burkina Faso


## Contributors
**Ajadi Sodiq Abayomi**, **Helyne Adamson**, **Sharon Christa**, **Elisabeth Lindner**

## Presentations


## Research question/objective

- How transferable are the drivers of urban heat islands across diverse climatic and urban contexts?
- Are the factors that drive extreme heat universal, or are they specific to a city's geography, climate, and development pattern?


## Background/Motivation

This comparative study replicates the methodology of the Da Nang study in Vietnam and applies it to Ouagadougou, Burkina Faso, to investigate urban heat hotspots in a Sahelian urban context. Specifically, it aims to evaluate the effectiveness of machine learning models in identifying hotspots during heatwave events, determine the most influential environmental and urban factors driving hotspot formation, and directly compare these results with those from Da Nang to evaluate which patterns are consistent and which differ due to Ouagadougou’s specific climate and urban structure.

The study is modeled after and builds upon the work by Hoang et al. (2025).

Hoang, ND., Huynh, TC. & Bui, DT. An interpretable machine learning framework for mapping hotspots and identifying their driving factors in urban environments during heat waves. Environ Monit Assess 197, 1017 (2025). https://doi.org/10.1007/s10661-025-14461-0


## Data



## Methods/Approach

### The study area
We selected the capital city of Ouagadougou, Burkina Faso, a major urban center in West Africa's Sahel region, as our comparative study area. Crucially, Ouagadougou shares key characteristics with Da Nang (e.g. similar latitude, population size, and a significant March-May 2024 heatwave), while representing a starkly different environment. Unlike coastal Da Nang's humid climate, Ouagadougou's semi-arid inland conditions create a climatic contrast, allowing us to investigate which urban heat drivers are universal or context-specific. This comparison can reveal how local climate modulates urban heat island effects.

### Research material
To characterize heatwave dynamics and intra-urban variations in temperature, we will collect and preprocess a combination of remote sensing and vector-based spatial datasets (summarised in Table 1). We will primarily use satellite imagery from Landsat 8 and Sentinel-2, digital eleva-
tion data from Copernicus, and road network data extracted from OpenStreetMap.

Table 1 - Research material and data sources

Surface reflectance and surface temperature products (30 m) from Landsat-8 and Sentinel-2 provide fine-scale spatial information of both land surface temperature (LST) and land use land cover (LULC) indices, including urban, vegetation, water, and soil indices (e.g. NDBI, NDVI, MNDWI, and Bare Soil Index). Topographical features are derived from the Copernicus global digital elevation model (DEM) at a resolution of 30m. OpenStreetMap (OSM) vector data is used for urban infrastructure features, such as proximity to roads and water bodies. Global Human Settlement Layer (GHSL) datasets are used for population metrics.

### The analysis methods
We will apply a machine learning approach to examine the precise spatial drivers of intra-urban heat patterns during extreme events and then test whether these drivers are consistent across two different urban environments. The study will replicate the XGBoost and SHAP analysis framework from Hoang et al. (2025) for Da Nang, Vietnam in 2024, and adapt it for the novel context of Ouagadougou, Burkina Faso, a rapidly urbanizing Sahelian city that also experienced severe heatwave events in 2024. We will test the generalizability of urban heat drivers by comparing the results from Ouagadougou with the published results from Da Nang, Vietnam. To build upon the work by Hoang, a causal model with pre-hoc weight assignment will be implemented before the training as in Yeboah et al. (2025), providing greater explanatory power to the study.

General method details:
- Heatwave events defined via ETCCDI indices (TX90p, WSDI).
- Anomalies computed vs. rural reference areas.
- Predictors: NDVI, NDBI, MNDWI, slope/elevation, green density, built-up share, distance to roads/water, population.
- Models: XGBoost + RF (stratified cross-validation, SHAP interpretability); pre-hoc causal model with weight assignment.

### Heat risk map
To test mitigation policies, we will digitally alter Ouagadougou's input maps - for example, artificially increasing the 'green space density' value by 10% in the city center - and then feed this modified map into our already-trained model to generate a new heat risk forecast. Comparing this new forecast to the original map will show us exactly how much and where the heat risk would be modified by an intervention.


## Literature 

Hoang, ND., Huynh, TC. & Bui, DT. An interpretable machine learning framework for mapping hotspots and identifying their driving factors in urban environments during heat waves. Environ Monit Assess 197, 1017 (2025). https://doi.org/10.1007/s10661-025-14461-0

Yeboah, E., Wang, G., Hagan, D.F.T. et al. A causal investigation of land use and land cover change on emerging urban heat island footprints in a mid-latitude region. Environ Dev Sustain (2025). https://doi.org/10.1007/s10668-025-06328-8

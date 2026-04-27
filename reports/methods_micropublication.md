# Methods: Micropublication Revision

**Original:** ~873 words / ~5,863 characters
**Shortened draft:** ~560 words (~36% reduction)

**Narrative focus:** Model comparison → SHAP importance → GCCM causal
validation. The key finding is that spectral indices (BSI, NDBI) correlate
most strongly with LST (r = +0.66) but show only symmetric bidirectional
coupling in GCCM, while built-up density (r = -0.10) is confirmed as
a unidirectional causal driver — an actionable lever for Sahelian
urban planners.

---

## Summary of changes from original

### CUT entirely

| What | Why |
|------|-----|
| LST scaling formula (`DN × 0.00341802 + 149.0`) | Standard USGS procedure; not needed |
| Band formulas for NDVI, NDBI, BSI | Canonical indices — name them and cite, or put in supplementary |
| Full hyperparameter values per model | Move to supplementary table |
| SHAP textbook explanation ("game-theoretic framework...") | Cite Lundberg & Lee; readers know SHAP |
| Road segment cleaning detail | Preprocessing detail for code repo |
| "No resampling techniques were applied" | Don't narrate what you didn't do |
| scikit-learn Pipeline standardization detail | Implementation detail |
| Tau sensitivity / Clifford-Dutilleul details | Not part of the narrative for this paper |

### REPHRASED to be more concise

| Where | What changed |
|-------|-------------|
| LST source | Dropped instrument acronyms (OLI/TIRS, OLI-2/TIRS-2) |
| QC | Consolidated 3 clauses into 1 sentence |
| Predictors | Dropped band numbers, kept names + what they capture |
| Model list | Dropped inline citations (move to reference list) |
| SHAP | 1 sentence instead of 3 |
| Software | One-liner at end of modelling section |

### KEPT (essential)

- LST source, resolution, temporal window, compositing
- Hotspot threshold (mu + 1sigma), prevalence (10.3%)
- All 8 predictor names, sources, and what they measure
- Circularity avoidance (predictors spectrally/temporally independent from LST)
- Three models, CV strategy, 70/30 split
- SHAP for feature importance (connects to GCCM validation narrative)
- GCCM: method, package, E=3, tau=1, N=2000, three causal criteria

### STRENGTHENED for narrative

| What | Why |
|------|-----|
| Added sentence linking SHAP → GCCM | Makes the pipeline explicit: SHAP identifies candidates, GCCM validates causality |
| Emphasized feature interpretability | Spectral indices share radiometric properties with LST (correlation ≠ causation); built-up/green density are physically independent and actionable |

---

## Issue flagged by scientific review

**"Standard UHI classification methodology" needs a citation.** Studies use
0.5sigma, 1sigma, 1.5sigma, or percentile thresholds. Cite the specific
paper you followed or drop "standard."

---

## Shortened draft (~560 words)

### Data

Land surface temperature (LST) was derived from Landsat 8 and 9 Collection 2 Level-2 Surface Temperature products (band ST_B10), composited across the March–May hot season from 2022 to 2024 to maximize cloud-free coverage. Scenes exceeding 20% cloud cover were excluded, per-pixel cloud and shadow masking was applied, and physically implausible values outside 20–60°C were rejected; a pixel-wise median composite was computed at 30 m resolution.

Thermal hotspots were defined as pixels exceeding the study-area mean by more than one standard deviation (LST > μ + 1σ; Zhang & Wang, 2008). Of the 613,847 valid pixels covering the Ouagadougou administrative boundary, approximately 10.3% were classified as hotspots.

Eight predictor variables were compiled from spectrally and temporally independent datasets to avoid analytical circularity with the Landsat-derived target (Table 1). All layers were resampled to a common 30 m UTM Zone 30N grid.

| Variable | Source | Processing |
|----------|--------|------------|
| NDVI (vegetation) | Sentinel-2 L2A, Mar–May 2024 | Cloud-masked median composite |
| NDBI (impervious surface) | Sentinel-2 L2A, Mar–May 2024 | Cloud-masked median composite |
| BSI (exposed soil) | Sentinel-2 L2A, Mar–May 2024 | Cloud-masked median composite |
| Elevation | Copernicus GLO-30 DEM | Native 30 m |
| Dist. to water | JRC Global Surface Water v1.4 | Euclidean distance; ≥70% occurrence threshold |
| Dist. to roads | OpenStreetMap | Euclidean distance |
| Built-up density | ESA WorldCover 2021 | Fraction within 90 m neighbourhood |
| Green space density | ESA WorldCover 2021 | Fraction within 90 m neighbourhood |

### Modelling

Three binary classifiers — XGBoost, Random Forest, and SVM (RBF kernel) — were trained on the eight predictors to classify hotspot occurrence; LST was excluded from all feature sets to prevent circularity. Data were split 70/30 train/test. Hyperparameters were optimized via five-fold cross-validated grid search (optimal values in Supplementary Table S1). Models were evaluated using accuracy, precision, recall, F1 score, and Cohen's Kappa on the held-out test set, and the best-generalizing model was selected for interpretability analysis.

To identify which predictors most strongly drive hotspot classification, feature importance was quantified using SHAP (Lundberg & Lee, 2017) via TreeExplainer. Because several high-ranking SHAP predictors (NDBI, BSI, NDVI) share radiometric properties with thermal emission — making high correlation with LST expected but not evidence of causation — we applied causal inference to distinguish genuine drivers from statistical proxies.

### Causal validation

To test whether SHAP-identified predictors causally influence LST or merely co-vary with it, we applied Geographical Convergent Cross Mapping (GCCM; Gao et al., 2023) as implemented in the spEDM R package (Lv, 2025). GCCM extends convergent cross mapping (Sugihara et al., 2012) to spatial cross-sections by reconstructing attractor manifolds from spatially lagged embeddings and testing whether one variable's state space can predict another's — a signature of causal influence under Takens' theorem. For each predictor–LST pair, bidirectional GCCM was run on the 150 m aggregated raster with embedding dimension E = 3 and spatial lag τ = 1 (150 m), using 2,000 randomly sampled prediction points. Causal direction was determined by three criteria following Gao et al.: (1) convergence (Kendall's τ > 0 for cross-map skill ρ vs. library size), (2) significance at the largest library size (p < 0.05), and (3) non-overlapping 95% Fisher-z confidence intervals between forward and reverse directions.

All modelling was implemented in Python (scikit-learn, XGBoost, shap); causal analysis used R (spEDM).




# TMP
 Urban heat islands threaten public health in rapidly urbanizing sub-Saharan Africa,
   yet the causal drivers of surface heating remain poorly understood in semi-arid   
  contexts. We mapped thermal hotspots in Ouagadougou, Burkina Faso during the       
  2022–2024 hot season using Landsat-derived land surface temperature (LST) and      
  compared three machine learning classifiers (XGBoost, Random Forest, SVM) trained  
  on eight landscape predictors. XGBoost achieved the best generalization (F1 = 0.70,
   Kappa = 0.67). SHAP analysis identified built-up density as the dominant
  predictor, while Geographical Convergent Cross Mapping (GCCM) confirmed it as a
  unidirectional causal driver of LST — unlike spectral indices (NDBI, BSI), which
  showed only bidirectional coupling despite strong correlations (r = +0.66).
  Contrary to findings in humid tropical cities, lower built-up density increased
  hotspot risk, as sparse development exposes bare soil to extreme solar heating.
  These results suggest compact urban form may mitigate surface heat in Sahelian
  cities.

Urban heat islands threaten public health in rapidly urbanizing sub-Saharan Africa,
   yet the causal drivers of surface heating remain poorly understood in semi-arid   
  contexts.
  We mapped thermal hotspots in Ouagadougou, Burkina Faso during the March–May hot 
  season (2022–2024) using Landsat-derived land surface temperature (LST) at 30 m    
  resolution. Three classifiers (XGBoost, Random Forest, SVM) were trained on eight  
  landscape predictors; XGBoost achieved the best generalization (F1 = 0.70, Kappa =
  0.67). SHAP analysis identified built-up density as the strongest predictor of
  hotspot occurrence. Geographical Convergent Cross Mapping (GCCM) confirmed built-up
   density and green space density as unidirectional causal drivers of LST, while
  spectral indices (NDBI, BSI) showed only symmetric bidirectional coupling despite
  correlating most strongly with LST (r = +0.66). Notably, lower built-up density
  increased hotspot risk — the opposite of patterns reported in humid tropical cities
   — because sparse development in this semi-arid context exposes bare soil to
  extreme solar heating. Compact urban form, rather than dispersed growth, may reduce
   surface heat exposure in Sahelian cities.


# Discussion
Hotspot formation during Ouagadougou's March-May 2024 heatwave season was dominated by built-up density, followed by distance to water, elevation, and NDBI. GCCM confirmed unidirectional causality for built-up density and green density, while NDBI and BSI showed bidirectional coupling. Replicating the methodology by Hoang et al. (2025) in semi-arid Sahelian Ouagadougou revealed a climate-dependent reversal with lower built-up density increasing hotspot risk, contrary to Da Nang in Vietnam. In  Ouagadougou, lower built-up density consists of unshaded bare soil with high solar absorption, leading to extreme surface temperature (Oke et al., 2017, Offerle et al., 2005). Consequently, higher built-up density provides a localized protective effect, likely due to micro-shading during the day and proximity to the centrally located reservoir (Linden, 2011), reversing the typical urban heat island patterns observed in temperate climates (Hoang et al., 2025, Offerle et al., 2005). Our findings demonstrate that urban heat mechanisms are not transferable across climate zones and suggest a refinement or reconceptualization of UHI definitions. In the context of Ouagadougou, urban planning should include compact development patterns using earth-based materials and encourage preservation of water bodies and creation of green spaces to minimize bare soil exposure. 
# Archived GCCM Run: tau10_detrend_nominal_neff

Archived on 2026-03-01 before modifying Clifford correction code.

## Why archived

The Clifford/Dutilleul N_eff correction was computed on **raw** (non-detrended)
raster values, but GCCM was run with `detrend=TRUE`. This mismatch means
N_eff is based on autocorrelation that includes the large-scale spatial trend,
which was already removed during GCCM. The correction is therefore
over-conservative (N_eff too low, CIs too wide).

The GCCM rho values (checkpoints) are correct. Only the statistical outputs
(CIs, p-values, direction labels in summary.csv) are affected.

## Run parameters

- **Date:** 2026-02-28 13:24 CET
- **Git hash:** 9692ff0
- **Code:** R/gccm_analysis.R + R/gccm_config.R
- **tau:** 10 (spatial lag = 1.5 km at 150m resolution)
- **E_RANGE:** 2:15
- **AGG_FACTOR:** 5 (30m -> 150m)
- **detrend:** TRUE
- **N_PRED:** 2000
- **Predictors:** built_density, green_density, distance_to_water,
  distance_to_roads, DEM, NDBI, BSI, NDVI
- **Clifford correction:** modified.ttest on RAW values (the issue)

## Key results (with nominal N_eff)

All predictors: "both significant" (CIs overlap for all pairs).
DEM negative control: correct direction (DEM->LST = 0.720 > LST->DEM = 0.616).

## Selected E values

| Variable | E |
|---|---|
| built_density | 12 |
| green_density | 10 |
| distance_to_water | 9 |
| distance_to_roads | 12 |
| DEM | 9 |
| NDBI | 10 |
| BSI | 11 |
| NDVI | 10 |
| LST | 9 |

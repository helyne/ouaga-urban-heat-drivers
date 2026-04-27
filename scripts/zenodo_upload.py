#!/usr/bin/env python3
"""Upload the supporting data deposit to Zenodo.

Creates a draft Zenodo deposit containing the processed raster stack and the
pre-fit ML model artifacts that accompany the publication. Metadata (title,
authors, license, description, keywords, link to GitHub) is set up front so
the draft is review-ready when the script finishes.

The script stops before publishing. Open the printed edit URL in a browser,
eyeball the draft, then click "Publish" yourself to finalize the DOI.

Usage
-----
Set the personal access token first (deposit:write + deposit:actions scopes).
Either export it directly or keep it in ``zenodo.env`` at the project root::

    export ZENODO_TOKEN=...
    python scripts/zenodo_upload.py

Or with the env file (auto-loaded if ZENODO_TOKEN is not in the environment)::

    # zenodo.env contains: ZENODO_TOKEN=...
    python scripts/zenodo_upload.py

Requires the ``requests`` package (already in requirements.txt via
earthengine-api).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ZENODO_API = "https://zenodo.org/api"

FILES = [
    PROJECT_ROOT / "data" / "processed" / "ouaga_aligned_stack.tif",
    PROJECT_ROOT / "models" / "Hotspotters_Models.zip",
]

DESCRIPTION = """\
<p>Processed 10-band raster stack and pre-fit machine-learning model artifacts (XGBoost, Random Forest, SVM) supporting the analysis in <em>"Reversal of UHI Drivers in a Sahelian City: Low Built-Up Density Increases Heat in Ouagadougou"</em> (Lindner, Adamson, Ajadi, Christa, Hagan; 2026).</p>

<p><strong>Files:</strong></p>
<ul>
<li><code>ouaga_aligned_stack.tif</code> &mdash; 10-band GeoTIFF at 30 m resolution covering the Ouagadougou administrative boundary, March&ndash;May 2022&ndash;2024 hot-season composite. Bands: NDVI, NDBI, BSI, DEM, distance_to_water, distance_to_roads, built_density, green_density, LST, hotspot. CRS: UTM Zone 30N.</li>
<li><code>Hotspotters_Models.zip</code> &mdash; Pre-fit binary classifiers (<code>xgb_model.pkl</code>, <code>rf_model.pkl</code>, <code>svm_model.pkl</code>) trained on the raster above using a 70/30 random train/test split with <code>random_state=42</code>. These artifacts reproduce the exact published F1, Cohen's &kappa;, and SHAP results.</li>
</ul>

<p>The raster is fully regenerable from public satellite sources (Landsat 8/9, Sentinel-2, Copernicus DEM GLO-30, JRC Global Surface Water, ESA WorldCover, OpenStreetMap) using the source code at <a href="https://github.com/helyne/ouaga-urban-heat-drivers">github.com/helyne/ouaga-urban-heat-drivers</a>.</p>
"""

METADATA = {
    "metadata": {
        "title": "Reversal of UHI Drivers in a Sahelian City \u2014 processed raster and pre-fit ML models",
        "upload_type": "dataset",
        "description": DESCRIPTION,
        "creators": [
            {
                "name": "Lindner, Elisabeth",
                "affiliation": "Heidelberg Institute of Global Health (HIGH), Heidelberg University Hospital, Heidelberg University",
                "orcid": "0009-0004-7031-5080",
            },
            {
                "name": "Adamson, Helyne",
                "affiliation": "Independent Researcher",
                "orcid": "0000-0002-3477-4296",
            },
            {
                "name": "Ajadi, Sodiq Abayomi",
                "affiliation": "University of Manchester",
                "orcid": "0000-0003-3275-1100",
            },
            {
                "name": "Christa, Sharon",
                "affiliation": "MIT Art Design and Technology University",
                "orcid": "0000-0001-6717-2200",
            },
            {
                "name": "Hagan, Daniel Fiifi Tawia",
                "affiliation": "Hydro-Climate Extremes Lab, Ghent University",
                "orcid": "0000-0003-3501-9783",
            },
        ],
        "license": "cc-by-4.0",
        "access_right": "open",
        "keywords": [
            "urban heat island",
            "machine learning",
            "causal inference",
            "remote sensing",
            "Ouagadougou",
            "Sahel",
            "GCCM",
            "XGBoost",
            "SHAP",
        ],
        "related_identifiers": [
            {
                "identifier": "https://github.com/helyne/ouaga-urban-heat-drivers",
                "relation": "isSupplementTo",
                "resource_type": "software",
            },
        ],
    }
}


def load_token() -> str:
    """Return the Zenodo access token from env var or zenodo.env."""
    token = os.environ.get("ZENODO_TOKEN")
    if token:
        return token.strip()

    env_file = PROJECT_ROOT / "zenodo.env"
    if not env_file.exists():
        sys.exit(
            "ERROR: ZENODO_TOKEN not in environment and zenodo.env not found. "
            "Either `export ZENODO_TOKEN=...` or create zenodo.env."
        )
    for line in env_file.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            stripped = stripped[len("export "):]
        if stripped.startswith("ZENODO_TOKEN"):
            _, _, value = stripped.partition("=")
            return value.strip().strip('"').strip("'")
    sys.exit("ERROR: ZENODO_TOKEN not found in zenodo.env.")


def check_files() -> None:
    """Bail early if any expected file is missing."""
    missing = [p for p in FILES if not p.exists()]
    if missing:
        for p in missing:
            print(f"ERROR: file not found: {p}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    check_files()
    token = load_token()
    auth = {"Authorization": f"Bearer {token}"}

    print("Creating draft deposit on Zenodo...")
    response = requests.post(
        f"{ZENODO_API}/deposit/depositions", json={}, headers=auth, timeout=30
    )
    response.raise_for_status()
    deposit = response.json()
    deposit_id = deposit["id"]
    bucket_url = deposit["links"]["bucket"]
    edit_url = deposit["links"]["html"]
    reserved_doi = deposit["metadata"]["prereserve_doi"]["doi"]
    print(f"  deposit ID:   {deposit_id}")
    print(f"  reserved DOI: {reserved_doi}")
    print()

    for path in FILES:
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f"Uploading {path.name} ({size_mb:.1f} MB)...")
        with open(path, "rb") as fh:
            up = requests.put(
                f"{bucket_url}/{path.name}",
                data=fh,
                headers=auth,
                timeout=600,
            )
        up.raise_for_status()
        print("  OK")

    print()
    print("Setting metadata...")
    meta = requests.put(
        f"{ZENODO_API}/deposit/depositions/{deposit_id}",
        json=METADATA,
        headers={**auth, "Content-Type": "application/json"},
        timeout=30,
    )
    meta.raise_for_status()
    print("  OK")

    print()
    print("=" * 64)
    print("Draft created. NOT YET PUBLISHED.")
    print()
    print(f"  Edit / review URL: {edit_url}")
    print(f"  Reserved DOI:      {reserved_doi}")
    print()
    print("Open the URL above, eyeball the draft, then click 'Publish' to")
    print("make the DOI permanent. Files are immutable after publish.")
    print("=" * 64)


if __name__ == "__main__":
    main()

# Belauri monthly PM2.5, 2024

Source: [SatPM V6.GL.03](https://www.satpm.org/v6-gl-03), licensed CC BY 4.0.
Original user portal: http://satpmdata.s3-website-us-east-1.amazonaws.com/#V6GL03/

The official provider confirms 1998–2024 monthly availability. We independently listed the public S3 bucket and extracted the twelve 2024 Asia-region fine-resolution NetCDF files. Every output month includes its exact official HTTPS source URL. The grid uses WGS84 coordinates, 0.01° cells, and PM25 in µg/m³. Source variable: `PM25`; source coordinate variables: `lat`, `lon`.

Boundary: OpenStreetMap Belauri municipality, relation 5927493, from `belauri-map/dist/data/boundary.geojson`.

Method: Extract cells whose square footprint intersects the municipality. For each month compute a weighted mean of valid, non-negative PM25 values using polygon-intersection area in longitude/latitude degrees multiplied by cosine(latitude), an approximation to physical overlap area appropriate for this small municipality. This is an area-weighted municipal estimate, not a population-weighted result. The output also includes all intersecting grid cells for map rendering; the UI should clip each cell to the municipality polygon. Monthly min/max refer to intersecting source-cell values.

Satellite PM2.5 estimates combine satellite aerosol retrievals, chemical transport modeling, and calibration against ground observations. They are not measurements from a Belauri monitor. The provider cautions that the nominal 0.01° grid cannot fully resolve fine-scale gradients because some input information is coarser.

Reproduction: `python3 data-research/extract_months.py`, requiring numpy, shapely, requests, and h5py. `remote_extract.py` implements cached HTTP range reads, downloading only the NetCDF regions needed. A full January file was also independently opened with netCDF4 to confirm units, shape, and one source-cell value (28.705 N, 80.345 E: 81.613464 µg/m³).

Validation: All 155 January cell values from remote byte-range extraction were independently compared against the fully downloaded January NetCDF using netCDF4. Maximum absolute difference was 0.000494 µg/m³, within the output rounding to three decimals.

Attribution: SatPM V6.GL.03, Atmospheric Composition Analysis Group (ACAG), Washington University in St. Louis / SatPM.org. Reference: Shen, S., Li, C., van Donkelaar, A., Jacobs, N., Wang, C., and Martin, R. V. (2024), “Enhancing Global Estimation of Fine Particulate Matter Concentrations by Including Geophysical a Priori Information in Deep Learning,” ACS ES&T Air, https://doi.org/10.1021/acsestair.3c00054. Dataset license: https://creativecommons.org/licenses/by/4.0/. Changes: subset to Belauri, intersected with municipal boundary, monthly area-weighted aggregation, rounded to 0.001 µg/m³, and converted to JSON/CSV. No endorsement by the original authors is implied. Boundary © OpenStreetMap contributors, https://www.openstreetmap.org/copyright (ODbL).

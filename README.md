# Belauri · Air & Places

A static map of Belauri municipality with facility layers, monthly 2024 PM2.5 data, and wind visualizations.

## Run locally

```sh
python3 -m http.server 8000 --directory belauri-map/dist
```

Open http://localhost:8000 in your browser.

## Project files

- `belauri-map/`: website, packaged data, and processing scripts. See its [README](belauri-map/README.md).
- `data-research/`: data extraction scripts and research outputs. See its [README](data-research/README.md) for sources, methods, and attribution.

Packaged archives, Python caches, and raw NetCDF downloads are excluded from version control.

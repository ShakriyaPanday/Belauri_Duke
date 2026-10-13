# Belauri · Air & Places

Buildless Leaflet website. Serve `dist/` with any static HTTP server.

Features: Belauri-only municipal map; four independently toggled facility layers; monthly 2024 PM2.5 chart, month selector, satellite grid overlay, and CSV export. Source/method information is available through “About the data”.

- Boundary and current facilities: OpenStreetMap contributors, ODbL. See `dist/data/provenance.json`.
- PM2.5: V6GL03 satellite-derived 2024 monthly Asia 0.01° files, with grid overlap-area-weighted means for Belauri. See `dist/data/pm25-2024.json` and `dist/data/pm-methods.md`.
- Browser fetches OpenStreetMap tiles and optional Google Fonts. All facility and PM data and Leaflet assets are packaged locally.
- Facilities are a current community-mapped inventory, not a historical inventory or proof of completeness. Clinics and health posts are included in the health layer.

Validation: JavaScript syntax check; valid municipality polygon; facility coordinates inside polygon; twelve monthly data records and finite PM values. Browser visual/interaction testing unavailable in the build environment.

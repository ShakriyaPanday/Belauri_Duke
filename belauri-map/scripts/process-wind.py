import json, math, calendar, sys
from pathlib import Path
raw=json.loads(Path(sys.argv[1]).read_text());h=raw['hourly'];months=[]
for month in range(1,13):
    rows=[(s,d) for t,s,d in zip(h['time'],h['wind_speed_10m'],h['wind_direction_10m']) if int(t[5:7])==month and s is not None and d is not None]
    assert len(rows)==calendar.monthrange(2024,month)[1]*24
    assert all(math.isfinite(s) and s>=0 and math.isfinite(d) and 0<=d<=360 for s,d in rows)
    u=sum(-s*math.sin(math.radians(d)) for s,d in rows)/len(rows)
    v=sum(-s*math.cos(math.radians(d)) for s,d in rows)/len(rows)
    speed=sum(s for s,d in rows)/len(rows); resultant=math.hypot(u,v)
    direction=(math.degrees(math.atan2(-u,-v))+360)%360 if resultant>1e-8 else None
    months.append(dict(month=month,from_degrees=round(direction,2) if direction is not None else None,toward_degrees=round((direction+180)%360,2) if direction is not None else None,mean_speed_ms=round(speed,3),resultant_speed_ms=round(resultant,3),directional_consistency=round(resultant/speed,3) if speed else 0,hours=len(rows)))
result=dict(year=2024,source='ERA5 via Open-Meteo Historical Weather API',source_url='https://open-meteo.com/en/docs/historical-weather-api',request_url='https://archive-api.open-meteo.com/v1/archive?latitude=28.72&longitude=80.35&start_date=2024-01-01&end_date=2024-12-31&hourly=wind_speed_10m,wind_direction_10m&models=era5&wind_speed_unit=ms&timezone=Asia%2FKathmandu',requested_location=dict(latitude=28.72,longitude=80.35),returned_grid=dict(latitude=raw['latitude'],longitude=raw['longitude']),timezone=raw['timezone'],height_m=10,resolution='0.25° (approximately 25 km)',license='CC BY 4.0',method='Hourly 10 m wind speeds and meteorological from-directions converted to eastward u=-speed*sin(direction) and northward v=-speed*cos(direction), then averaged by calendar month in Asia/Kathmandu. From-direction calculated using atan2(-mean_u,-mean_v); arrow points 180° opposite, toward the direction of travel. Mean speed is the scalar hourly average. Directional consistency is resultant speed divided by mean speed (0=opposing directions cancel; 1=uniform direction). A value below 0.1 is labelled variable and the arrow is hidden. Single regional ERA5 grid estimate, not a municipal spatial mean or station observation.',months=months)
Path('dist/data/wind-2024.json').write_text(json.dumps(result,indent=2))
print([(m['month'],m['from_degrees'],m['directional_consistency']) for m in months])

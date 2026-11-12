-- Preview the data
SELECT * FROM weather_raw LIMIT 10;

-- Average maximum temperature and total rainfall per city
SELECT city,
       ROUND(AVG(temp_max_c), 1) AS avg_max_temp,
       ROUND(SUM(rain_mm), 1)    AS total_rain
FROM weather_raw
GROUP BY city;

-- Hottest day per city (window function)
SELECT city, obs_date, temp_max_c
FROM (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY city ORDER BY temp_max_c DESC) AS rn
  FROM weather_raw
) t
WHERE rn = 1;

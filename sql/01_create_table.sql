-- Run in Athena (region: ap-southeast-2)
CREATE DATABASE weather_lake;

-- External table over the raw CSV files in S3. Replace <bucket> with your bucket name.
CREATE EXTERNAL TABLE weather_raw (
  city string,
  obs_date string,
  temp_max_c double,
  temp_min_c double,
  rain_mm double
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 's3://<bucket>/raw/weather/'
TBLPROPERTIES ('skip.header.line.count'='1');

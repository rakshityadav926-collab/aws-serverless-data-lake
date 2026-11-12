# AWS Serverless Data Lake

A small serverless data pipeline on AWS. A Lambda function pulls public weather data into S3, and Athena runs SQL on it.

**Status: in progress.** The checklist below shows what is built and what is not.

## Architecture

```
Open-Meteo API --> AWS Lambda (Python) --> S3 raw/ (JSON) --> S3 clean/ (Parquet) --> Athena (SQL)
                          |
                  EventBridge schedule (daily)
                          |
                  CloudWatch logs
```

## Data source

[Open-Meteo](https://open-meteo.com/) public weather API. It is free, needs no API key and is open to non-commercial use. I use daily temperature and rainfall for a few Indian cities. No employer or private data is used.

## Plan and status

- [ ] AWS account safety: MFA, IAM user, billing alert
- [ ] S3 bucket with `raw/` and `clean/` prefixes
- [ ] Athena table over the raw data and first SQL queries
- [ ] Lambda function that fetches data and writes JSON to `raw/`
- [ ] Convert raw JSON to Parquet in `clean/`
- [ ] EventBridge daily schedule
- [ ] CloudWatch logging and error alerts
- [ ] Screenshots and example queries in this README

## Planned SQL (Athena)

- Average temperature by city and month
- Hottest day per city using `ROW_NUMBER()`
- Rolling 7-day average rainfall using window functions

## Project structure

```
aws-serverless-data-lake/
  lambda/        Lambda function code
  sql/           Athena queries
  docs/          screenshots and notes
  README.md
```

## What I am learning from this

How S3, Lambda, IAM and Athena work together, and how to design a raw-to-clean data lake layout.

## Author

Rakshit Yadav, Gurugram. [LinkedIn](https://linkedin.com/in/rakshit-yadav-8612a7367)

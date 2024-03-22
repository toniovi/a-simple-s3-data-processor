# Demo of the MVP: Step-by-Step
## The S3 Bucket
- Let's suppose we have this aws bucket:
  - <img width="466" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/e501447f-d995-480f-92e7-850c456996da">
- With some `events.csv` files:
  - <img width="501" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/1ab88e5a-08e4-4938-896f-294970a1247e">

## The Codespaces
- First, Create a Codespaces on this repo
  - <img width="527" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/951ecfde-10da-4e14-9a0f-cf46e1305536">
- _and wait for installation to finish:_
  - <img width="540" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/1be4797f-5842-4bfb-a4c3-587e3cd1bf00">

## Dagster
- Run `task dagster_dev`
- Go to your port 3000
  - <img width="474" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/41d27400-321e-4380-b8b1-271fbe654f1f">
- Your two Dagster `assets` have not yet been _"materialized"_:
  - <img width="1316" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/7238e2e9-499f-4735-981b-952320ddb182">
- And your `sensor` is not running:
  - <img width="1036" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/7fb905fb-c905-416b-8616-62f8c0aeeeb1">
> The sensor (to automatically _"materialize"_ all files in the bucket) is not yet functional
> So let's just manually _"materialize"_ one of the csv files:
  - <img width="813" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/53556bdf-2f6a-456c-9595-4a0b9991d99a">
- Let's say, the january 2022 file:
  - <img width="688" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/cf9cae0f-27a6-4e80-b15a-ab7f9eb91a4c">
- Launch the run:
  - <img width="741" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/6b18c754-5056-4da2-bf56-3a5bd7f247c8">

## The result
> A `pickled` Pandas dataframe, available to any downstream process, stored in `/workspaces/a-simple-s3-data-processor/storage/read_monthly_csv/2022_01`
<img width="886" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/5d08c373-a145-45b1-a91d-50ba9883adb6">
<img width="692" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/42be2291-4037-409b-bc04-853dc5dde1e5">


# Presenting you my Workflow 

## Some Project Evolutions I've Identified
- Config a [Run Coordinator](https://docs.dagster.io/deployment/run-coordinator) for being able to accept concurring runs.
- ...

## On Friday 22/03/2024
Started refactoring from this inspiration: https://dagster.io/blog/dynamic-partitioning
It so much better (almost perfectly) fits the requirements!

### DONE! Refacto is in the `feature_dynamic_partitioning` branch: ready to start testing and merge if everything OK

## How To — Installing your own Dev Workbench and Contributing to the Project
- You can use github Codespaces to quickly dev in this project, everything's been configured to install and start a functioning machine with Dagster (and all necessary dependencies) installed:
  - <img width="716" alt="image" src="https://github.com/toniovi/a-simple-s3-data-processor/assets/131332847/6a32acd4-a0de-4210-a5d0-3d82e45c042f">
- Once the machine has finished installing, you can run Dagster in dev mode.
I've configured a taskfile task for this, you can simply run:
  - `task dagster_dev`



# **The Project**: A simple S3 data processor — PoC

Hereunder the Technical Requirements Document (TRD), which offers a comprehensive overview of the requirements for this Proof of Concept (PoC).

The actual implementation will be coded specifically in the **dagster_orchestration** folder of this repo.

The entire structure of this repository is designed to address all of the _Future Improvements_ requirements outlined in the TRD.

# Technical Requirements Document (TRD) for this Proof of Concept (PoC)

## Objective
The objective of this PoC is to automate the process of retrieving and processing large CSV files from an S3 bucket. The processed data should be made available for efficient data analysis.

## Input
The input to the system is a S3 bucket address.

## Output
The output of the system is a processed Pandas DataFrame.

## Functional Requirements
- The system must process a file publicly hosted in an S3 bucket for a given "year-month" value passed as a parameter.
- The system must make the processed data available for performing efficient data analyses.
- The system should be designed to be easily improved to support future needs such as full automation and recurrent and periodic retrieval and processing of data without any external action.

## Non-Functional Requirements
- The system should be able to handle large CSV files.
- The system should be able to process the data efficiently and quickly.

## Future Improvements
- Industrialize the system: The system should be designed in a way that it can be easily industrialized.
- Host the system: The system should be hosted in a way that it can handle large amounts of data and high traffic.
- Deploy the system to production: The system should be designed in a way that it can be easily deployed to production.
- Make the system recurring: The system should be designed in a way that it can be easily made to run recurrently and periodically.
- Monitor the runs: The system should have a monitoring system in place to monitor the runs and be warned in case of failure.

## Data Storage
- The data is stored in an S3 bucket.
- The data is stored in a monthly format with one directory per year and one subdirectory per month (e.g., "2021/01", "2021/02", etc.).
- The data files are always named "events.csv".

## Data Analysis
The system should establish a technological framework that enables various analyses on the data, such as determining the number of events per year/month/day, identifying the most active users and companies, etc.

## Technology Stack
- Python: As development language.
- AWS S3: For data storage.
- Dagster: For data orchestration and automation.
- Pydantic _(on Dagster)_: For data validation and settings management.
- Pandas: For data manipulation and analysis.

## Development Approach
- The development will be iterative, with regular communication and feedback.
- The focus will be on building a functional MVP and making the project as understandable as possible.



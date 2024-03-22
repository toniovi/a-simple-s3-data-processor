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



# A simple S3 data processor — PoC

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



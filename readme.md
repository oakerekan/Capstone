# Brazilian E-Commerce ETL Pipeline

![Alt text](https://github.com/oakerekan/Capstone/blob/main/assets/Images/Untitled-2024-08-16-2129.png)


### Project Overview</b>
This project uses the Brazilian E-Commerce dataset to create an end-to-end ETL (Extract, Transform, Load) pipeline. The goal is to develop a pipeline that ingests data into PostgreSQL, processes and transforms it, and then loads it into Google BigQuery. The project also includes answering analytical questions based on the transformed data.

### Tools and Technologies
PostgreSQL: For data storage and ingestion.
Docker & Docker Compose: For containerization and managing services.
Apache Airflow: For orchestrating the ETL process.
dbt: For data transformation and modeling.
Google BigQuery: For data warehousing and analysis.


Project Steps
Step 1: Data Ingestion into PostgreSQL
1.1 Download the Dataset
Download the Brazilian E-Commerce dataset from Kaggle.
1.2 Setup PostgreSQL Database
Docker Setup:
Create a docker-compose.yml file for PostgreSQL and airflow.

The docker compose file which was shared by the tutor was run as docker-compose up -d to initialise the container. 
After this instantiation. The Docker compose volume and dependent file were created to help with the process.

The next step is to log in to the airflow UI on hostocalhost:8081/login with username and password as airflow. 

The dag was created to run the Postgres to GCS to Big Query Orchestration required for this project. 

The credential where supplied when making a connection within the airflow UI under the admin to enable connection with the Google cloud platfomr.
The Service account json was supplied as expected.

ANd the Dag were run as expected. 

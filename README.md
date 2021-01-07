# Airflow_ELT_Pipeline
 <br>Author: Hiroaki Oshima    
 Date: Jan 4, 2021<br><br>
# About This Project 

<br><br>I implemented this project as a part of Udacity Data Engineering Nanodegree program. This project is a data pipeline/ workflow management implemented with widely used open-source software Apache Airflow. It will sequentially execute an Extract Load Transform Process (ELT) step by step and manage its workflow. Airflow will load log data of application and song data from AWS S3 into Data Warehouse on AWS Redshift. On Redshift server, airflow will transform the raw data and store into more normalized tables such as songs, users, artists, or dates  so that analytics team will be able to run various queries. Finally, upon finishing the transformation, airflow will run unit tests on each table that was created to ensure the data quality is good<br><br>

# Files
####  DAG
 1. **dags/aws_etl.py**:  airflow dag files contain every task and their dependencies
 ####  Operators
 
 1. **plugins/myoperators/stage_redshift.py**: Custome operator which stage the log data on S3 server on Redshift Server <br><br>
 2. **plugins/myoperators/load_fact**: Custome operator that transform the staged log data into fact tables<br><br>
 3. **plugins/myoperators/load_dimensions**: Custom operator that transform the staged tables into dimension tables<br><br>
 4. **plugins/myoperators/data_quality**: Ensure given columns of given tables were transformed successfully <br><br>

# Data Pipeline Workflow
Dag Image:
![pipeline image](https://i.ibb.co/khRdXwz/Screen-Shot-2021-01-04-at-6-49-38-PM.png)<br><br>
**Before Running Airflow**: I created a data warehouse cluster on AWS Redshift and assign the host address into an airflow variable along with the security credentials <br> <br>
**Create Tables** uses postgres operator to create tables on AWS Redshift and drop old tables if exists. The SQL queries and detail schemas is in plugin/helpers/sql_queries.py <br><br>
**Stage_tables** load log and song JSON data onto Redshift server from S3 <br><br>
**Load_fact_table** transform the staged data into the fact table *songplays* <br><br>
**Load_dim_table** creates 4 dimension tables transformed from the fact table <br><br>
**Run_table_quality_check** make sure the table that was just created is not broken <br><br>


##  Table Schemas

#### Fact Table

1.  **songplays**  - records in event data associated with song plays i.e. records with page  `NextSong`
    -   _songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent_

#### Dimension Tables

2.  **users**  - users in the app
    -   _user_id, first_name, last_name, gender, level_
3.  **songs**  - songs in music database
    -   _song_id, title, artist_id, year, duration_
4.  **artists**  - artists in music database
    -   _artist_id, name, location, lattitude, longitude_
5.  **time**  - timestamps of records in  **songplays**  broken down into specific units
    -   _start_time, hour, day, week, month, year, weekday_

There is one fact table, songplay, which is the log data of users' playing songs on apps. There are four in dimension tables which individually store information abour users, songs, artists, and time. This normalized format allow analytics team to run various queries, such as they can specify the gender of users, location or times when they play songs.

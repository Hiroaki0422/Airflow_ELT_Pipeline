from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from airflow.operators.postgres_operator import PostgresOperator
from helpers import SqlQueries, CreateQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'hiroo',
    'start_date': datetime(2021,1,3),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=3),
    'catchup': False,
    'email':['kifa0422@gmail.com'],
    'email_on_failure':False,
    'email_on_retry':False
}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval= '@daily'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_tables = PostgresOperator(
    task_id='Create_tables',
    dag=dag,
    sql=CreateQueries.all_tables_create,
    postgres_conn_id='redshift'
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    redshift_conn_id='redshift',
    table='staging_events',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend',
    s3_key='log_data',
    json='s3://udacity-dend/log_json_path.json'
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    redshift_conn_id='redshift',
    table='staging_songs',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend',
    s3_key='song_data',
    json='auto'
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='songplays',
    sql=SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='users',
    sql=SqlQueries.user_table_insert
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='songs',
    sql=SqlQueries.song_table_insert
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='artists',
    sql=SqlQueries.artist_table_insert
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='time',
    sql=SqlQueries.time_table_insert
)

songplay_quality_checks =DataQualityOperator(
    task_id='Run_songplay_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    table='songplays',
    columns=['playid', 'sessionid']
)

user_quality_checks =DataQualityOperator(
    task_id='Run_user_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    table='users',
    columns=['userid']
)

song_quality_checks =DataQualityOperator(
    task_id='Run_song_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    table='songs',
    columns=['songid']
)

artist_quality_checks =DataQualityOperator(
    task_id='Run_artist_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    table='artists',
    columns=['artistid']
)

time_quality_checks =DataQualityOperator(
    task_id='Run_time_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    table='time',
    columns=['start_time', 'year']
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> create_tables
create_tables >> [stage_events_to_redshift, stage_songs_to_redshift]

stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table

load_songplays_table >> [load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table]

load_songplays_table >> songplay_quality_checks
load_user_dimension_table >> user_quality_checks
load_song_dimension_table >> song_quality_checks
load_artist_dimension_table >> artist_quality_checks
load_time_dimension_table >> time_quality_checks

[songplay_quality_checks, user_quality_checks, song_quality_checks, artist_quality_checks, \
 time_quality_checks] >> end_operator





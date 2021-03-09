from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql="",
                 truncate=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql
        self.truncate = truncate

    def execute(self, context):
        self.log.info('LoadDimensionOperator Running....')

        # Establish Connection
        redshit = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Run SQL Script to load dimension table
        # If truncate, delete the table first
        if self.truncate == True:
            redshit.run(f'DELETE FROM {self.table}')
        
        redshit.run(f'INSERT INTO {self.table} {self.sql}')

        self.log.info(f'table {self.table} is loaded')


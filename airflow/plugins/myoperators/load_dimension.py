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
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql

    def execute(self, context):
        self.log.info('LoadDimensionOperator Running....')

        # Establish Connection
        redshit = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Run SQL Script to load dimension table 
        redshit.run(f'INSERT INTO {self.table} {self.sql}')

        self.log.info(f'table {self.table} is loaded')


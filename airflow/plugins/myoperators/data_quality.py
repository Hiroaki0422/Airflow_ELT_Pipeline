from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 table = "",
                 columns = [],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.columns = columns.copy()

    def execute(self, context):
        self.log.info('DataQualityOperator Running')

        # Establish the connection
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Running query to see if given table is empry or not
        row_count = redshift.get_records(f'SELECT COUNT(*) FROM {self.table}')[0][0]
        if row_count < 1:
            raise ValueError(f'table {self.table} has no records')

        # Running query to see if given columns of the table is empry or not
        for column in self.columns:
            result = redshift.get_records(f'SELECT COUNT(*) FROM {self.table} WHERE {column} IS NOT NULL')[0][0]
            if result < 1:
                raise ValueError(f'column {self.table}.{column} has no records')
            self.log.info(f'column {self.table}.{column} has {result} records out of {row_count}')

        self.log.info('Data Quality Check for {self.table} is complete')



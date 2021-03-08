from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import operator

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self, redshift_conn_id="", dq_checks=[], *args, **kwargs):
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.dq_checks = dq_checks.copy()

    def execute(self, context):
        self.log.info('Starting Data Validation')

        # Establish the connection
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Running tests for tables raise value error if failed
        for test in self.dq_checks:
            self.log.info(f'Running {test["testsql"]}')
            result = redshift.get_records(test['testsql'])[0][0]

            if not test['op'](result, test['expected']):
                raise ValueError(f'Data Quality Check failed query:{test["testsql"]}, expected:{test["expected"]}, got:{result}')

        self.log.info('Data Validation Complete, Congraduation')


from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    
    sql_copy = """
                COPY {}
                FROM '{}'
                ACCESS_KEY_ID '{}'
                SECRET_ACCESS_KEY '{}'
                region 'us-west-2'
                JSON '{}'
               """
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 aws_credentials_id="",
                 s3_bucket="",
                 s3_key="",
                 json="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json = json

    def execute(self, context):
        self.log.info('Dev mode staging to AWS redshift')
        
        # get credentials of aws
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        
        # Establish connection with redshifrt
        redshift = PostgresHook(self.redshift_conn_id)
        
        # get path to s3 bucket
        # rendered_key = self.s3_key.format(**context)
        s3_path = 's3://{}/{}/'.format(self.s3_bucket, self.s3_key)
        
        # format the sql statement
        delete_sql = 'DELETE FROM {}'.format(self.table)
        stage_sql = StageToRedshiftOperator.sql_copy.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.json
            )
        
        # execute sql statements on redshift
        self.log.info('Staging.....')
        
        redshift.run(delete_sql)
        redshift.run(stage_sql)
        
        self.log.info('Staging Complete')
        
        
        
        
        
        
        
        






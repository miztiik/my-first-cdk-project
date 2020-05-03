from aws_cdk import core
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_s3_notifications as _s3_notifications


class ServerlessEventProcessorArchitectureWithS3EventsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Add your stack resources below):
        # Create an S3 Bucket for storing our web store assets
        kk_store = _s3.Bucket(
            self,
            "kkStore",
            versioned=True
        )

        # DynamoDB Table
        kk_store_assets_table = _dynamodb.Table(
            self,
            "kkStoreAssetsDDBTable",
            table_name="kk_store_assets_tables",
            partition_key=_dynamodb.Attribute(
                name="_id",
                type=_dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Read Lambda Code
        try:
            with open("advanced_use_cases/lambda_src/s3_event_processor.py", mode="r") as f:
                kk_store_processor_fn_code = f.read()
        except OSError:
            print("Unable to read Lambda Function Code")

        # Deploy the lambda function
        kk_store_processor_fn = _lambda.Function(
            self,
            "kkStoreProcessorFn",
            function_name="kk_store_processor_fn",
            description="Process store events and update DDB",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(
                kk_store_processor_fn_code
            ),
            timeout=core.Duration.seconds(3),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "DDB_TABLE_NAME": f"{kk_store_assets_table.table_name}"
            }
        )

        # Add DynamoDB Write Privileges To Lambda
        kk_store_assets_table.grant_read_write_data(kk_store_processor_fn)

        # Create Custom Loggroup
        kk_store_lg = _logs.LogGroup(
            self,
            "kkStoreLogGroup",
            log_group_name=f"/aws/lambda/{kk_store_processor_fn.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_DAY
        )

        # Create s3 notification for lambda function
        kk_store_backend = _s3_notifications.LambdaDestination(
            kk_store_processor_fn
        )

        # Assign notification for the s3 event type (ex: OBJECT_CREATED)
        kk_store.add_event_notification(
            _s3.EventType.OBJECT_CREATED, kk_store_backend
        )

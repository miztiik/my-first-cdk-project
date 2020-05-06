from aws_cdk import core
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_event_sources as _lambda_event_sources


class ServerlessDdbStreamProcessorArchitectureWithSteamsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Add your stack resources below):
        # DynamoDB Table
        api_db = _dynamodb.Table(
            self,
            "apiDDBTable",
            partition_key=_dynamodb.Attribute(
                name="_id",
                type=_dynamodb.AttributeType.STRING
            ),
            stream=_dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Read Lambda Code
        try:
            with open("advanced_use_cases/lambda_src/dynamodb_stream_processor.py", mode="r") as f:
                ddb_stream_processor_fn_code = f.read()
        except OSError:
            print("Unable to read lambda function code")

        # Deploy the lambda function
        ddb_stream_processor_fn = _lambda.Function(
            self,
            "ddbStreamProcessorFn",
            function_name="ddb_stream_processor_fn",
            description="Process DDB Streaming data events",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(
                ddb_stream_processor_fn_code
            ),
            timeout=core.Duration.seconds(3),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO"
            }
        )

        # Create New DDB Stream Event Source
        ddb_stream_event_source = _lambda_event_sources.DynamoEventSource(
            table=api_db,
            starting_position=_lambda.StartingPosition.TRIM_HORIZON,
            bisect_batch_on_error=True
        )

        # Attach DDB Event Source As Lambda Trigger
        ddb_stream_processor_fn.add_event_source(ddb_stream_event_source)

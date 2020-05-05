from aws_cdk import core
from aws_cdk import aws_kinesis as _kinesis
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_lambda_event_sources as _lambda_event_sources



class ServerlessStreamProcessorArchitectureWithKinesisStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Add your stack resources below):
        # Create Kinesis Data Stream
        stream_data_pipe = _kinesis.Stream(
            self,
            "streamDataPipe",
            retention_period=core.Duration.hours(24),
            shard_count=1,
            stream_name="data_pipe"
        )
        

        # Create an S3 Bucket for storing streaming data events
        stream_data_store = _s3.Bucket(
            self,
            "streamDataLake",
            removal_policy=core.RemovalPolicy.DESTROY
        )


        # Read Lambda Code
        try:
            with open("advanced_use_cases/lambda_src/stream_record_consumer.py",mode="r") as f:
                stream_consumer_fn_code = f.read()
        except OSError:
            print("Unable to read lambda function code")


        # Deploy the lambda function
        stream_consumer_fn = _lambda.Function(
            self,
            "streamConsumerFn",
            function_name="stream_consumer_fn",
            description="Process streaming data events from kinesis and store in S3",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(
                stream_consumer_fn_code
            ),
            timeout=core.Duration.seconds(3),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL":"INFO",
                "BUCKET_NAME": f"{stream_data_store.bucket_name}"
            }
        )

        # Update Lambda Permissions To Use Stream
        stream_data_pipe.grant_read(stream_consumer_fn)
        
        # Add permissions to lambda to write to S3
        roleStmt1 = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources=[
                f"{stream_data_store.bucket_arn}/*"
            ],
            actions=[
                "s3:PutObject"
            ]
        )
        roleStmt1.sid="AllowLambdaToWriteToS3"
        stream_consumer_fn.add_to_role_policy(roleStmt1)


        # Create Custom Loggroup for Consumer
        stream_consumer_lg = _logs.LogGroup(
            self,
            "streamConsumerLogGroup",
            log_group_name=f"/aws/lambda/{stream_consumer_fn.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_DAY
        )


        # Create New Kinesis Event Source
        stream_data_pipe_event_source = _lambda_event_sources.KinesisEventSource(
            stream=stream_data_pipe,
            starting_position=_lambda.StartingPosition.LATEST,
            batch_size=1
        )


        # Attach Kinesis Event Source To Lambda
        stream_consumer_fn.add_event_source(stream_data_pipe_event_source)

        ########################################
        #######                          #######
        #######   Stream Data Producer   #######
        #######                          #######
        ########################################
        
        # Read Lambda Code
        try:
            with open("advanced_use_cases/lambda_src/stream_data_producer.py", mode="r") as f:
                data_producer_fn_code = f.read()
        except OSError:
            print("Unable to read lambda function code")

        # Deploy the lambda function
        data_producer_fn = _lambda.Function(
            self,
            "streamDataProducerFn",
            function_name="data_producer_fn",
            description="Produce streaming data events and push to Kinesis stream",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(
                data_producer_fn_code
            ),
            timeout=core.Duration.seconds(60),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL":"INFO",
                "STREAM_NAME":f"{stream_data_pipe.stream_name}"
            }
        )


        # Grant our Lambda Producer privileges to write to Kinesis Data Stream
        stream_data_pipe.grant_read_write(data_producer_fn)


        # Create Custom Loggroup for Producer
        data_producer_lg = _logs.LogGroup(
            self,
            "dataProducerLogGroup",
            log_group_name=f"/aws/lambda/{data_producer_fn.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_DAY
        )


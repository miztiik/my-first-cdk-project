from aws_cdk import core
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_apigateway as _apigw


class ServerlessRestApiArchitectureStack(core.Stack):

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
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Read Lambda Code
        try:
            with open("advanced_use_cases/lambda_src/rest_api_backend.py", mode="r") as f:
                api_backend_fn_code = f.read()
        except OSError:
            print("Unable to read lambda function code")

        # Deploy the lambda function
        api_backend_fn = _lambda.Function(
            self,
            "apiBackendFn",
            function_name="api_backend_fn",
            description="Process API events from APIGW and ingest to DDB",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(
                api_backend_fn_code
            ),
            timeout=core.Duration.seconds(3),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "DDB_TABLE_NAME": f"{api_db.table_name}"
            }
        )

        # Add DynamoDB Write Privileges To Lambda
        api_db.grant_read_write_data(api_backend_fn)

        # Create Custom Loggroup
        api_backend_lg = _logs.LogGroup(
            self,
            "apiBackendLoggroup",
            log_group_name=f"/aws/lambda/{api_backend_fn.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_DAY
        )

        # Add API GW front end for the Lambda
        api_01 = _apigw.LambdaRestApi(
            self,
            "apiFrontEnd",
            rest_api_name="api-frontend",
            handler=api_backend_fn,
            proxy=False
        )

        user_name = api_01.root.add_resource("{user_name}")
        add_user_likes = user_name.add_resource("{likes}")
        add_user_likes.add_method("GET")

        # Output API GW Url
        output_1 = core.CfnOutput(
            self,
            "ApiUrl",
            value=f"{add_user_likes.url}",
            description="User a browser to access this url, Replace {user_name} and {likes} with your own values"
        )

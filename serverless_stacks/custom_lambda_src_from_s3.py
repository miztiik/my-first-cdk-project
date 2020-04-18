from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_s3 as _s3
from aws_cdk import core


class CustomLambdaSrcFromS3Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Import an S3 Bucket):
        konstone_bkt = _s3.Bucket.from_bucket_attributes(self,
                                                         "konstoneAssetsBucket",
                                                         bucket_name="konstone-assets-bkt")

        # Create Lambda function with source code from S3 Bucket
        konstone_fn = _lambda.Function(self,
                                       "konstoneFunction",
                                       function_name="konstone_fn",
                                       runtime=_lambda.Runtime.PYTHON_3_7,
                                       handler="konstone_processor.lambda_handler",
                                       code=_lambda.S3Code(
                                           bucket=konstone_bkt,
                                           key="lambda_src/konstone_processor.zip"
                                       ),
                                       timeout=core.Duration.seconds(2),
                                       reserved_concurrent_executions=1
                                       )

        # Create Custom Loggroup
        # /aws/lambda/function-name
        konstone_lg = _logs.LogGroup(self,
                                     "konstoneLoggroup",
                                     log_group_name=f"/aws/lambda/{konstone_fn.function_name}",
                                     removal_policy=core.RemovalPolicy.DESTROY,
                                     retention=_logs.RetentionDays.ONE_WEEK
                                     )

from aws_cdk import (
    aws_s3 as _s3,
    aws_iam as _iam,
    core
)


class MyFirstCdkProjectStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        mybucket = _s3.Bucket(
            self,
            "myBucketId1"
        )

        _iam.Group(self,
                   "gid")

        output_1 = core.CfnOutput(
            self,
            "myBucketOutput1",
            value=mybucket.bucket_name,
            description=f"My first CDK Bucket",
            export_name="myBucketOutput1"
        )

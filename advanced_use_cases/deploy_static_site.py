from aws_cdk import core
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_s3_deployment as _s3_deployment


class DeployStaticSiteStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 Bucket):
        static_site_assets_bkt = _s3.Bucket(
            self,
            "assetsBucket",
            versioned=True,
            public_read_access=True,
            website_index_document="index.html",
            website_error_document="404.html",
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Add assets to static site bucket
        add_assets_to_site = _s3_deployment.BucketDeployment(
            self,
            "deployStaticSiteAssets",
            sources=[
                _s3_deployment.Source.asset(
                    "advanced_use_cases/static_assets"
                )
            ],
            destination_bucket=static_site_assets_bkt
        )

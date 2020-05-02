from aws_cdk import core
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_s3_deployment as _s3_deployment
from aws_cdk import aws_cloudfront as _cloudfront


class DeployCloudfrontOaiStaticSiteStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 Bucket):
        static_site_assets_bkt = _s3.Bucket(
            self,
            "assetsBucket",
            versioned=True,
            # public_read_access=True,
            # website_index_document="index.html",
            # website_error_document="404.html",
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

        # Create OAI for Cloudfront
        static_site_oai = _cloudfront.OriginAccessIdentity(
            self,
            "staticSiteOai",
            comment=f"OAI for static site from stack:{core.Aws.STACK_NAME}"
        )

        # Deploy Cloudfront Configuration: Connecting OAI with static asset bucket
        cf_source_configuration = _cloudfront.SourceConfiguration(
            s3_origin_source=_cloudfront.S3OriginConfig(
                s3_bucket_source=static_site_assets_bkt,
                origin_access_identity=static_site_oai
            ),
            behaviors=[
                _cloudfront.Behavior(
                    is_default_behavior=True,
                    compress=True,
                    allowed_methods=_cloudfront.CloudFrontAllowedMethods.ALL,
                    cached_methods=_cloudfront.CloudFrontAllowedCachedMethods.GET_HEAD
                )
            ]
        )

        # Create Cloudfront Distribution
        static_site_distribution = _cloudfront.CloudFrontWebDistribution(
            self,
            "staticSiteCfDistribution",
            comment="CDN for static website",
            origin_configs=[cf_source_configuration],
            price_class=_cloudfront.PriceClass.PRICE_CLASS_100
        )

        # Output Cloudfront Url
        output_1 = core.CfnOutput(
            self,
            "CloudfrontUrl",
            value=f"{static_site_distribution.domain_name}",
            description="The domain name of the static site"
        )

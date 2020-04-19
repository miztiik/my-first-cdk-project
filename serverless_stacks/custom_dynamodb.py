from aws_cdk import core
from aws_cdk import aws_dynamodb as _dynamodb


class CustomDynamoDBStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB: Key-Value Database):

        konstone_assets_table = _dynamodb.Table(
            self,
            "konstoneAssetsDDBTable",
            partition_key=_dynamodb.Attribute(
                name="id",
                type=_dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            server_side_encryption=True
        )

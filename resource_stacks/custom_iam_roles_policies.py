from aws_cdk import core
from aws_cdk import aws_ssm as _ssm
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_secretsmanager as _secretsmanager


class CustomRolesPoliciesStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Let us IAM Users & Groups):
        user1_pass = _secretsmanager.Secret(self,
                                            "user1Pass",
                                            description="Password for User1",
                                            secret_name="user1_pass"
                                            )

        # Add User1 with SecretsManager Password
        user1 = _iam.User(self, "user1",
                          password=user1_pass.secret_value,
                          user_name="user1"
                          )

        # Add IAM Group
        konstone_group = _iam.Group(self,
                                    "konStoneGroup",
                                    group_name="konstone_group"
                                    )

        # Add User to Group
        konstone_group.add_user(user1)

        # Add Managed Policy to Group
        konstone_group.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess")
        )
        # SSM parameter 1
        param1 = _ssm.StringParameter(
            self,
            "parameter1",
            description="Keys To KonStone",
            parameter_name="/konstone/keys/fish",
            string_value="130481",
            tier=_ssm.ParameterTier.STANDARD
        )

        # SSM parameter 2
        param2 = _ssm.StringParameter(
            self,
            "parameter2",
            description="Keys To KonStone",
            parameter_name="/konstone/keys/fish/gold",
            string_value="130482",
            tier=_ssm.ParameterTier.STANDARD
        )

        # Grant Konstone group permission to Param 1
        param1.grant_read(konstone_group)

        # Grant Group to LIST ALL SSM Parameters in Console
        grpStmt1 = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ssm:DescribeParameters"
            ]
        )
        grpStmt1.sid = "DescribeAllParametersInConsole"

        # Add Permissions To Group
        konstone_group.add_to_policy(grpStmt1)

        # Create IAM Role
        konstone_ops_role = _iam.Role(
            self,
            'konstoneOpsRole',
            assumed_by=_iam.AccountPrincipal(f"{core.Aws.ACCOUNT_ID}"),
            role_name="konstone_ops_role"
        )

        # Create Managed Policy & Attach to Role
        list_ec2_policy = _iam.ManagedPolicy(
            self,
            "listEc2Instances",
            description="list ec2 isntances in the account",
            managed_policy_name="list_ec2_policy",
            statements=[
                _iam.PolicyStatement(
                    effect=_iam.Effect.ALLOW,
                    actions=[
                        "ec2:Describe*",
                        "cloudwatch:Describe*",
                        "cloudwatch:Get*"
                    ],
                    resources=["*"]
                )
            ],
            roles=[
                konstone_ops_role
            ]
        )

        # Login Url Autogeneration
        output_1 = core.CfnOutput(self,
                                  "user1LoginUrl",
                                  description="LoginUrl for User1",
                                  value=f"https://{core.Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
                                  )

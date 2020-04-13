#!/usr/bin/env python3

from aws_cdk import core

from resource_stacks.custom_vpc import CustomVpcStack
from resource_stacks.custom_ec2 import CustomEc2Stack
from resource_stacks.custom_ec2_with_instance_profile import CustomEc2InstanceProfileStack
from resource_stacks.custom_ec2_with_latest_ami import CustomEc2LatestAmiStack
from resource_stacks.custom_ec2_with_ebs_piops import CustomEc2PiopsStack
from resource_stacks.custom_parameters_secrets import CustomParametersSecretsStack
from resource_stacks.custom_iam_users_groups import CustomIamUsersGroupsStack
from resource_stacks.custom_iam_roles_policies import CustomRolesPoliciesStack

from app_stacks.vpc_stack import VpcStack
from app_stacks.web_server_stack import WebServerStack


app = core.App()

env_prod = core.Environment(account="830058508584", region="us-east-1")

# Custom VPC Stack
# CustomVpcStack(app, "my-custom-vpc-stack", env=env_prod)

# Custom Ec2 Stack
# CustomEc2Stack(app, "my-web-server-stack", env=env_prod)

# Custom EC2 InstaceProfileStack
# CustomEc2InstanceProfileStack(app, "web-server-stack", env=env_prod)

# Custom EC2 Instace with Latest AMI Stack
# CustomEc2LatestAmiStack(app, "web-server-latest-ami-stack", env=env_prod)

# EC2 with Provisioned IOPS
# piops_stack = CustomEc2PiopsStack(app, "ec2-with-piops-stack")

# Application Stack ASG and ALB
# vpc_stack = VpcStack(app, "multi-tier-app-vpc-stack")
# ec2_stack = WebServerStack(
#     app, "multi-tier-app-web-server-stack", vpc=vpc_stack.vpc)

# Create SSM Parameter & AWS Secrets Manager Secrets
# params_secrets_stack = CustomParametersSecretsStack(
#     app,
#     "custom-parameters-secrets-stack",
#     description="Create SSM Parameter & AWS Secrets Manager Secrets"
# )

# Create IAM User & Groups
# iam_users_groups_stack = CustomIamUsersGroupsStack(
#     app,
#     "custom-iam-users-groups-stack",
#     description="Create IAM User & Groups"
# )

# Create IAM Roles & Policies
custom_iam_roles_policies = CustomRolesPoliciesStack(
    app,
    "custom-iam-roles-policies-stack",
    description="Create IAM Roles & Policies"
)


# Stack Level Tagging
core.Tag.add(app, key="Owner",
             value=app.node.try_get_context('owner'))
core.Tag.add(app, key="OwnerProfile",
             value=app.node.try_get_context('github_profile'))
core.Tag.add(app, key="GithubRepo",
             value=app.node.try_get_context('github_repo_url'))
core.Tag.add(app, key="ToKnowMore",
             value=app.node.try_get_context('youtube_profile'))


app.synth()

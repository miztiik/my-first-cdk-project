#!/usr/bin/env python3

from aws_cdk import core

from my_first_cdk_project.my_first_cdk_project_stack import MyArtifactBucketStack

env_US = core.Environment(region="us-east-1")
env_EUROPE = core.Environment(region="eu-east-1")
app = core.App()
MyArtifactBucketStack(app, "myDevStack", env=env_US)
MyArtifactBucketStack(app, "myProdStack", is_prod=True, env=env_US)

app.synth()

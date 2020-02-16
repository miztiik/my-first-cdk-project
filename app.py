#!/usr/bin/env python3

from aws_cdk import core

from my_first_cdk_project.my_first_cdk_project_stack import MyArtifactBucketStack

env_US = core.Environment(account="904521749370", region="us-east-1")
env_EU = core.Environment(account="313487964768", region="eu-west-1")
app = core.App()
MyArtifactBucketStack(app, "myDevStack", env=env_US)
MyArtifactBucketStack(app, "myProdStack", is_prod=True, env=env_EU)

app.synth()

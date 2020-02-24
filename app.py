#!/usr/bin/env python3

from aws_cdk import core

from resource_stacks.custom_vpc import CustomVpcStack


app = core.App()

CustomVpcStack(app, "my-custom-vpc-stack")

app.synth()

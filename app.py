#!/usr/bin/env python3

from aws_cdk import core

from resource_stacks.custom_vpc import CustomVpcStack


app = core.App()

CustomVpcStack(app, "my-custom-vpc-stack")

core.Tag.add(app, key="stack-name", value="network-stack")
core.Tag.add(app, key="support-team",
             value=app.node.try_get_context('envs')['prod']['support-email'])


app.synth()

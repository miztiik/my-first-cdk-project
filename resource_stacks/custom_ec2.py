from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core


class CustomEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = _ec2.Vpc.from_lookup(self,
                                   "importedVPC",
                                   vpc_id="vpc-d0a193aa")

        web_server = _ec2.Instance(self,
                                   "webServerId",
                                   instance_type=_ec2.InstanceType(
                                       instance_type_identifier="t2.micro"),
                                   instance_name="WebServer001",
                                   machine_image=_ec2.MachineImage.generic_linux(
                                       {"us-east-1": "ami-0fc61db8544a617ed"}
                                   ),
                                   vpc=vpc,
                                   vpc_subnets=_ec2.SubnetSelection(
                                       subnet_type=_ec2.SubnetType.PUBLIC
                                   )
                                   )

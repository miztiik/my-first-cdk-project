from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core


class CustomEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = _ec2.Vpc.from_lookup(self,
                                   "importedVPC",
                                   vpc_id="vpc-d0a193aa")

        # Read BootStrap Script
        with open("bootstrap_scripts/install_httpd.sh", mode="r") as file:
            user_data = file.read()

        # WebServer Instance 001
        web_server = _ec2.Instance(self,
                                   "WebServer001Id",
                                   instance_type=_ec2.InstanceType(
                                       instance_type_identifier="t2.micro"),
                                   instance_name="WebServer001",
                                   machine_image=_ec2.MachineImage.generic_linux(
                                       {"us-east-1": "ami-0fc61db8544a617ed"}
                                   ),
                                   vpc=vpc,
                                   vpc_subnets=_ec2.SubnetSelection(
                                       subnet_type=_ec2.SubnetType.PUBLIC
                                   ),
                                   user_data=_ec2.UserData.custom(user_data)
                                   )

        output_1 = core.CfnOutput(self,
                                  "webServer001Ip",
                                  description="WebServer Public Ip Address",
                                  value=f"http://{web_server.instance_public_ip}")

        # Allow Web Traffic to WebServer
        web_server.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description="Allow Web Traffic"
        )

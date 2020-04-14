from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_elasticloadbalancingv2 as _elbv2
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_autoscaling as _autoscaling
from aws_cdk import core


class WebServer3TierStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Read BootStrap Script):
        try:
            with open("app_db_stack/user_data/deploy_app.sh", mode="r") as file:
                user_data = file.read()
        except OSError:
            print('Unable to read UserData script')

        linux_ami = _ec2.AmazonLinuxImage(generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                          edition=_ec2.AmazonLinuxEdition.STANDARD,
                                          virtualization=_ec2.AmazonLinuxVirt.HVM,
                                          storage=_ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                          )

        # Create Application Load Balancer
        alb = _elbv2.ApplicationLoadBalancer(
            self,
            "myAlbId",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name="WebServerAlb"
        )

        # Allow ALB to receive internet traffic
        alb.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80),
            description="Allow Internet access on ALB Port 80"
        )

        # Add Listerner to ALB
        listener = alb.add_listener("listernerId",
                                    port=80,
                                    open=True)

        # Webserver IAM Role
        web_server_role = _iam.Role(self, "webServerRoleId",
                                    assumed_by=_iam.ServicePrincipal(
                                        'ec2.amazonaws.com'),
                                    managed_policies=[
                                        _iam.ManagedPolicy.from_aws_managed_policy_name(
                                            'AmazonSSMManagedInstanceCore'
                                        ),
                                        _iam.ManagedPolicy.from_aws_managed_policy_name(
                                            'AmazonS3ReadOnlyAccess'
                                        )
                                    ])

        # Create AutoScaling Group with 2 EC2 Instances.
        self.web_server_asg = _autoscaling.AutoScalingGroup(self,
                                                            "webServerAsgId",
                                                            vpc=vpc,
                                                            vpc_subnets=_ec2.SubnetSelection(
                                                                subnet_type=_ec2.SubnetType.PRIVATE
                                                            ),
                                                            instance_type=_ec2.InstanceType(
                                                                instance_type_identifier="t2.micro"),
                                                            machine_image=linux_ami,
                                                            role=web_server_role,
                                                            min_capacity=2,
                                                            max_capacity=2,
                                                            #    desired_capacity=2,
                                                            user_data=_ec2.UserData.custom(
                                                                user_data)
                                                            )

        # Allows ASG Security Group receive traffic from ALB
        self.web_server_asg.connections.allow_from(alb, _ec2.Port.tcp(80),
                                                   description="Allows ASG Security Group receive traffic from ALB")

        # Add AutoScaling Group Instances to ALB Target Group
        listener.add_targets("listenerId", port=80,
                             targets=[self.web_server_asg])

        # Output of the ALB Domain Name
        output_alb_1 = core.CfnOutput(self,
                                      "albDomainName",
                                      value=f"http://{alb.load_balancer_dns_name}",
                                      description="Web Server ALB Domain Name")

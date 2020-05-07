from aws_cdk import core
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_ecs as _ecs
from aws_cdk import aws_ecs_patterns as _ecs_patterns


class ContainerizedMicroserviceArchitectureWithEcsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Add your stack resources below):
        # Create VPC
        vpc = _ec2.Vpc(
            self,
            "microServiceVpc",
            max_azs=2,
            nat_gateways=1
        )

        # Create ECS Cluster
        micro_service_cluster = _ecs.Cluster(
            self,
            "webServiceCluster",
            vpc=vpc
        )

        # Define ECS Cluster Capacity
        micro_service_cluster.add_capacity(
            "microServiceAutoScalingGroup",
            instance_type=_ec2.InstanceType("t2.micro")
        )

        # Deploy Container in the micro Service & Attach a LoadBalancer
        load_balanced_web_service = _ecs_patterns.ApplicationLoadBalancedEc2Service(
            self,
            "webService",
            cluster=micro_service_cluster,
            memory_reservation_mib=512,  # Soft Limit
            task_image_options={
                "image": _ecs.ContainerImage.from_registry("mystique/web-server"),
                "environment": {
                    "ENVIRONEMNT": "PROD"
                }
            }
        )

        # Output Web Service Url
        output_1 = core.CfnOutput(
            self,
            "webServiceUrl",
            value=f"{load_balanced_web_service.load_balancer.load_balancer_dns_name}",
            description="Acces the web service url from your browser"
        )

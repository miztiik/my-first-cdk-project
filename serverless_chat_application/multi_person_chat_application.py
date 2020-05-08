from aws_cdk import core
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_ecs as _ecs
from aws_cdk import aws_ecs_patterns as _ecs_patterns


class MultiPersonChatApplicationStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here):
        # Create VPC
        vpc = _ec2.Vpc(
            self,
            "chatAppVpc",
            max_azs=2,
            nat_gateways=1
        )

        # Create Fargate Cluster
        chat_app_cluster = _ecs.Cluster(
            self,
            "chatAppCluster"
        )

        # Create chat service as Fargate Task
        chat_app_task_def = _ecs.FargateTaskDefinition(
            self,
            "chatAppTaskDef"
        )

        # Create Container Definition
        chat_app_container = chat_app_task_def.add_container(
            "chatAppContainer",
            image=_ecs.ContainerImage.from_registry(
                "mystique/fargate-chat-app:latest"
            ),
            environment={
                "github": "https://github.com/miztiik"
            }
        )

        # Add Port Mapping to Container, Chat app runs on Port 3000
        chat_app_container.add_port_mappings(
            _ecs.PortMapping(container_port=3000, protocol=_ecs.Protocol.TCP)
        )

        # Deploy Container in the micro Service & Attach a LoadBalancer
        chat_app_service = _ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "Service",
            cluster=chat_app_cluster,
            task_definition=chat_app_task_def,
            assign_public_ip=False,
            public_load_balancer=True,
            listener_port=80,
            desired_count=1,
            service_name="ChatApp"
        )

        # Output Chat App Url
        output_1 = core.CfnOutput(
            self,
            "chatAppServiceUrl",
            value=f"http://{chat_app_service.load_balancer.load_balancer_dns_name}",
            description="Access the chat app url from your browser"
        )

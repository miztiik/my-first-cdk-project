from aws_cdk import core
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_ecs as _ecs
from aws_cdk import aws_ecs_patterns as _ecs_patterns
from aws_cdk.aws_applicationautoscaling import Schedule


class ServerlessBatchProcessorArchitectureWithFargateStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Add your stack resources below):
        # Create VPC
        vpc = _ec2.Vpc(
            self,
            "batchProcessorVpc",
            max_azs=2,
            nat_gateways=1
        )

        # Create Fargate Cluster
        batch_processor_cluster = _ecs.Cluster(
            self,
            "batchProcessorCluster",
            vpc=vpc
        )

        # Deploy Batch Processing Container Task in Fargate with Cloudwatch Event Schedule
        batch_process_task = _ecs_patterns.ScheduledFargateTask(
            self,
            "batchProcessor",
            cluster=batch_processor_cluster,
            scheduled_fargate_task_image_options={
                "image": _ecs.ContainerImage.from_registry("mystique/batch-job-runner"),
                "memory_limit_mib": 512,
                "cpu": 256,
                "environment": {
                    "name": "TRIGGEr",
                    "value": "CloudWatch Events"
                }
            },
            schedule=Schedule.expression("rate(2 minutes)")
        )

from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_sns as _sns
from aws_cdk import aws_sns_subscriptions as _subs
from aws_cdk import core
from aws_cdk import aws_cloudwatch as _cloudwatch
from aws_cdk import aws_cloudwatch_actions as _cloudwatch_actions


class CustomEc2WithAlarmsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create SNS Topic for Operations Team):
        konstone_ops_team = _sns.Topic(self,
                                       "konstoneOpsTeam",
                                       display_name="KonStone 24x7 On Watsapp? Support",
                                       topic_name="konstoneOpsTeam"
                                       )

        # Add Subscription to SNS Topic
        konstone_ops_team.add_subscription(
            _subs.EmailSubscription("konstone@gmail.com")
        )

        # Create a MultiAZ VPC):
        vpc = _ec2.Vpc(
            self,
            "konstoneVpcId",
            cidr="10.0.0.0/24",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="public", subnet_type=_ec2.SubnetType.PUBLIC
                )
            ]
        )

        # Read EC2 BootStrap Script
        try:
            with open("bootstrap_scripts/install_httpd.sh", mode="r") as file:
                user_data = file.read()
        except OSError:
            print('Unable to read UserData script')

        # Get the latest ami
        amzn_linux_ami = _ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            storage=_ec2.AmazonLinuxStorage.EBS,
            virtualization=_ec2.AmazonLinuxVirt.HVM
        )

        # WebServer Instance
        web_server = _ec2.Instance(self,
                                   "WebServer004Id",
                                   instance_type=_ec2.InstanceType(
                                       instance_type_identifier="t2.micro"),
                                   instance_name="WebServer004",
                                   machine_image=amzn_linux_ami,
                                   vpc=vpc,
                                   vpc_subnets=_ec2.SubnetSelection(
                                       subnet_type=_ec2.SubnetType.PUBLIC
                                   ),
                                   user_data=_ec2.UserData.custom(user_data)
                                   )

        # Allow Web Traffic to WebServer
        web_server.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description="Allow Web Traffic"
        )

        # Add permission to web server instance profile
        web_server.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore")
        )

        # Read Lambda Code
        try:
            with open("serverless_stacks/lambda_src/konstone_processor.py", mode="r") as f:
                konstone_fn_code = f.read()
        except OSError:
            print("Unable to read Lambda Function Code")

        # Simple Lambda Function to return event
        konstone_fn = _lambda.Function(self,
                                       "konstoneFunction",
                                       function_name="konstone_function",
                                       runtime=_lambda.Runtime.PYTHON_3_7,
                                       handler="index.lambda_handler",
                                       code=_lambda.InlineCode(
                                           konstone_fn_code),
                                       timeout=core.Duration.seconds(3),
                                       reserved_concurrent_executions=1,
                                       environment={
                                           "LOG_LEVEL": "INFO",
                                           "AUTOMATION": "SKON"
                                       }
                                       )

        # EC2 Metric for Avg. CPU
        ec2_metric_for_avg_cpu = _cloudwatch.Metric(
            namespace="AWS/EC2",
            metric_name="CPUUtilization",
            dimensions={
                "InstanceId": web_server.instance_id
            },
            period=core.Duration.minutes(5)
        )

        # Low CPU Alarm for Web Server
        low_cpu_alarm = _cloudwatch.Alarm(
            self,
            "lowCPUAlarm",
            alarm_description="Alert if CPU is less than 10%",
            alarm_name="low-cpu-alarm",
            actions_enabled=True,
            metric=ec2_metric_for_avg_cpu,
            threshold=10,
            comparison_operator=_cloudwatch.ComparisonOperator.LESS_THAN_OR_EQUAL_TO_THRESHOLD,
            evaluation_periods=1,
            datapoints_to_alarm=1,
            period=core.Duration.minutes(5),
            treat_missing_data=_cloudwatch.TreatMissingData.NOT_BREACHING
        )

        # Inform SNS on EC2 Alarm State
        low_cpu_alarm.add_alarm_action(
            _cloudwatch_actions.SnsAction(
                konstone_ops_team
            )
        )

        # Create Lambda Alarm
        konstone_fn_error_alarm = _cloudwatch.Alarm(
            self,
            "konstoneFunctionErrorAlarm",
            metric=konstone_fn.metric_errors(),
            threshold=2,
            evaluation_periods=1,
            datapoints_to_alarm=1,
            period=core.Duration.minutes(5)
        )

        # Inform SNS on Lambda Alarm State
        konstone_fn_error_alarm.add_alarm_action(
            _cloudwatch_actions.SnsAction(
                konstone_ops_team
            )
        )

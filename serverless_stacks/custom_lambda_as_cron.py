from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_events as _events
from aws_cdk import aws_events_targets as _targets


class CustomLambdaAsCronStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Serverless Event Processor using Lambda):

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

        # Run Every day at 18:00 UTC
        six_pm_cron = _events.Rule(
            self,
            "sixPmRule",
            schedule=_events.Schedule.cron(
                minute="0",
                hour="18",
                month="*",
                week_day="MON-FRI",
                year="*"
            )
        )

        # Setup Cron Based on Rate
        # Run Every 3 Minutes
        run_every_3_minutes = _events.Rule(
            self,
            "runEvery3Minutes",
            schedule=_events.Schedule.rate(core.Duration.minutes(3))
        )

        # Add Lambda to CW Event Rule
        six_pm_cron.add_target(_targets.LambdaFunction(konstone_fn))
        run_every_3_minutes.add_target(_targets.LambdaFunction(konstone_fn))

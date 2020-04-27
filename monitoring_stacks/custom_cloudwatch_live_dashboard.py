from aws_cdk import aws_cloudwatch as _cloudwatch
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import core


class CustomCloudwatchLiveDashboardStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Read Lambda Code):
        try:
            with open("serverless_stacks/lambda_src/konstone_custom_metric_log_generator.py", mode="r") as f:
                konstone_custom_metric_fn_code = f.read()
        except OSError:
            print("Unable to read Lambda Function Code")

        konstone_custom_metric_fn = _lambda.Function(
            self,
            "konstoneFunction",
            function_name="konstone_custom_metric_fn",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(
                konstone_custom_metric_fn_code),
            timeout=core.Duration.seconds(
                3),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "PERCENTAGE_ERRORS": "75"
            }
        )

        # Create Custom Loggroup
        # /aws/lambda/function-name
        konstone_custom_metric_lg = _logs.LogGroup(
            self,
            "konstoneLoggroup",
            log_group_name=f"/aws/lambda/{konstone_custom_metric_fn.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_DAY,
        )

        # Create Custom Metric Namespace
        third_party_error_metric = _cloudwatch.Metric(
            namespace=f"third-party-error-metric",
            metric_name="third_party_error_metric",
            label="Total No. of Third Party API Errors",
            period=core.Duration.minutes(1),
            statistic="Sum"
        )

        # Create Custom Metric Log Filter
        third_party_error_metric_filter = _logs.MetricFilter(
            self,
            "thirdPartyApiErrorMetricFilter",
            filter_pattern=_logs.FilterPattern.boolean_value(
                "$.third_party_api_error", True),
            log_group=konstone_custom_metric_lg,
            metric_namespace=third_party_error_metric.namespace,
            metric_name=third_party_error_metric.metric_name,
            default_value=0,
            metric_value="1"
        )

        # Create Third Party Error Alarm
        third_party_error_alarm = _cloudwatch.Alarm(
            self,
            "thirdPartyApiErrorAlarm",
            alarm_description="Alert if 3rd party API has more than 2 errors in the last two minutes",
            alarm_name="third-party-api-alarm",
            metric=third_party_error_metric,
            comparison_operator=_cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            threshold=2,
            evaluation_periods=2,
            datapoints_to_alarm=1,
            period=core.Duration.minutes(1),
            treat_missing_data=_cloudwatch.TreatMissingData.NOT_BREACHING
        )

        # Create CloudWatch Dashboard
        konstone_dashboard = _cloudwatch.Dashboard(
            self,
            id="konstoneDashboard",
            dashboard_name="Konstone-App-Live-Dashboard"
        )

        # Add Lambda Function Metrics to Dashboard
        konstone_dashboard.add_widgets(
            _cloudwatch.Row(
                _cloudwatch.GraphWidget(
                    title="Backend-Invocations",
                    left=[
                        konstone_custom_metric_fn.metric_invocations(
                            statistic="Sum",
                            period=core.Duration.minutes(1)
                        )
                    ]
                ),
                _cloudwatch.GraphWidget(
                    title="Backend-Errors",
                    left=[
                        konstone_custom_metric_fn.metric_errors(
                            statistic="Sum",
                            period=core.Duration.minutes(1)
                        )
                    ]
                )
            )
        )

        # Add 3rd Party API Error to Dashboard
        konstone_dashboard.add_widgets(
            _cloudwatch.Row(
                _cloudwatch.SingleValueWidget(
                    title="Third Party API Errors",
                    metrics=[third_party_error_metric]
                )
            )
        )

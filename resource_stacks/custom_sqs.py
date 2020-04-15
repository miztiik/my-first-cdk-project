from aws_cdk import core
from aws_cdk import aws_sqs as _sqs


class CustomSqsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Konstone Hot SQS Queue):
        konstone_Queue = _sqs.Queue(self,
                                    "konstoneQueue",
                                    queue_name="konstone_queue.fifo",
                                    fifo=True,
                                    encryption=_sqs.QueueEncryption.KMS_MANAGED,
                                    retention_period=core.Duration.days(4),
                                    visibility_timeout=core.Duration.seconds(
                                        45)
                                    )

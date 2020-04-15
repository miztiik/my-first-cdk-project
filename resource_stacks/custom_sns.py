from aws_cdk import core
from aws_cdk import aws_sns as _sns
from aws_cdk import aws_sns_subscriptions as _subs


class CustomSnsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create SNS Topic):

        konstone_topic = _sns.Topic(self,
                                    "konstoneHotTopics",
                                    display_name="Latest topics on KonStone",
                                    topic_name="konstoneHotTopic"
                                    )

        # Add Subscription to SNS Topic
        konstone_topic.add_subscription(
            _subs.EmailSubscription("konstone@gmail.com")
        )

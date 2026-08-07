from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.subscriber.configure import (
    configure_subscriber_template,
)


class TestConfigureSubscriberTemplate(TestCase):

    def test_configure_subscriber_template(self):
        device = Mock()

        result = configure_subscriber_template(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'subscriber templating',
                'subscriber authorization enable',
            ]
        )

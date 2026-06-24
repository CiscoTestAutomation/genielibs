import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.subscriber.configure import configure_subscriber_service_session_accounting


class TestConfigureSubscriberServiceSessionAccounting(unittest.TestCase):

    def test_configure_subscriber_service_session_accounting(self):
        device = Mock()
        result = configure_subscriber_service_session_accounting(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "subscriber service session-accounting"
        )

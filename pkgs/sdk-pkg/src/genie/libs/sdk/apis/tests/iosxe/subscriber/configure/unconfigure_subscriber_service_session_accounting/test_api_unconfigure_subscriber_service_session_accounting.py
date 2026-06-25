import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.subscriber.configure import unconfigure_subscriber_service_session_accounting


class TestUnconfigureSubscriberServiceSessionAccounting(unittest.TestCase):

    def test_unconfigure_subscriber_service_session_accounting(self):
        device = Mock()
        result = unconfigure_subscriber_service_session_accounting(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "no subscriber service session-accounting"
        )

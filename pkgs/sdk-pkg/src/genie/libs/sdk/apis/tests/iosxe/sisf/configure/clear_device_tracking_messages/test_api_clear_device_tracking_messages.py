from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sisf.configure import (
    clear_device_tracking_messages,
)


class TestClearDeviceTrackingMessages(TestCase):

    def test_clear_device_tracking_messages(self):
        device = Mock()

        result = clear_device_tracking_messages(device)

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            'clear device-tracking messages',
        )

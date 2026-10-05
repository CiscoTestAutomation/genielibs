from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sisf.configure import (
    configure_device_tracking_on_interface,
)


class TestConfigureDeviceTrackingOnInterface(TestCase):

    def test_configure_device_tracking_on_interface(self):
        device = Mock()

        result = configure_device_tracking_on_interface(
            device,
            'TwentyFiveGigE1/0/1',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'interface TwentyFiveGigE1/0/1',
            'device-tracking',
        ])

from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sisf.configure import (
    remove_device_tracking_policy,
)


class TestRemoveDeviceTrackingPolicy(TestCase):

    def test_remove_device_tracking_policy(self):
        device = Mock()
        result = remove_device_tracking_policy(
            device=device,
            client_policy_name='pol1',
            server_policy_name='pol2',
        )
        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'no device-tracking policy pol1',
            'no device-tracking policy pol2',
        ])

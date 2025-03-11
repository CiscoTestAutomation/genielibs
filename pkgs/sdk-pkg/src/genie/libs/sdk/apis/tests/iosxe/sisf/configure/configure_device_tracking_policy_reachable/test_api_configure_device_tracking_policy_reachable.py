from unittest import TestCase
from genie.libs.sdk.apis.iosxe.sisf.configure import configure_device_tracking_policy_reachable
from unittest.mock import Mock


class TestConfigureDeviceTrackingPolicyReachable(TestCase):

    def test_configure_device_tracking_policy_reachable(self):
        self.device = Mock()
        result = configure_device_tracking_policy_reachable(self.device, 'tracking', 'enable', 10)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['device-tracking policy tracking', 'tracking enable reachable-lifetime 10'],)
        )

import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import hw_module_beacon_RP_active_standby


class TestHwModuleBeaconRpActiveStandby(unittest.TestCase):

    def test_hw_module_beacon_RP_active_standby(self):
        device = Mock()

        result = hw_module_beacon_RP_active_standby(device, 'active', 'on')

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('hw-module beacon RP active on',)
        )
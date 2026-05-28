import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import hw_module_beacon_rp_toggle


class TestHwModuleBeaconRpToggle(unittest.TestCase):

    def test_hw_module_beacon_rp_toggle(self):
        device = Mock()

        result = hw_module_beacon_rp_toggle(device, 'R0', 'on')

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('hw-module beacon R0 on',)
        )
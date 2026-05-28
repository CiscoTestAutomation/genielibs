import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import hw_module_beacon_slot_on_off


class TestHwModuleBeaconSlotOnOff(unittest.TestCase):

    def test_hw_module_beacon_slot_on_off(self):
        device = Mock()

        result = hw_module_beacon_slot_on_off(device, 1, 'on')

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('hw-module beacon slot 1 on',)
        )
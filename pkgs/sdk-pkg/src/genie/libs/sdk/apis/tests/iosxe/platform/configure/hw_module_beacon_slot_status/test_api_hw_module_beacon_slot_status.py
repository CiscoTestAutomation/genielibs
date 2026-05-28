import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import hw_module_beacon_slot_status


class TestHwModuleBeaconSlotStatus(unittest.TestCase):

    def test_hw_module_beacon_slot_status(self):
        device = Mock()

        device.execute.return_value = 'BLUE'

        result = hw_module_beacon_slot_status(device, 0)

        self.assertEqual(result, 'BLUE')
import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import hw_module_beacon_rp_active_standby_status


class TestHwModuleBeaconRpActiveStandbyStatus(unittest.TestCase):

    def test_hw_module_beacon_rp_active_standby_status(self):
        device = Mock()

        device.execute.return_value = 'Beacon LED: BLUE'

        result = hw_module_beacon_rp_active_standby_status(device, 'active')

        self.assertEqual(result, 'Beacon LED: BLUE')
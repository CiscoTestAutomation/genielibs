import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import hw_module_beacon_rp_active_standby_status


class TestHwModuleBeaconRpActiveStandbyStatus(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ENC:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ENC']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_hw_module_beacon_rp_active_standby_status(self):
        result = hw_module_beacon_rp_active_standby_status(self.device, 'active')
        expected_output = 'BLUE'
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import hw_module_beacon_RP_active_standby


class TestHwModuleBeaconRpActiveStandby(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          4-slot:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9400
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['4-slot']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_hw_module_beacon_RP_active_standby(self):
        result = hw_module_beacon_RP_active_standby(self.device, 'active', 'on')
        expected_output = None
        self.assertEqual(result, expected_output)

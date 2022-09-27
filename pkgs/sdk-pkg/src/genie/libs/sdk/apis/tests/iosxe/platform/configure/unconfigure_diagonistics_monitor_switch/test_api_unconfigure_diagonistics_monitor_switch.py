import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_diagonistics_monitor_switch


class TestUnconfigureDiagonisticsMonitorSwitch(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack12-gala-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack12-gala-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_diagonistics_monitor_switch(self):
        result = unconfigure_diagonistics_monitor_switch(self.device, 1, 'DiagThermalTest', '00:03:00', 20, 1)
        expected_output = None
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_fnf_monitor_on_interface


class TestUnconfigureFnfMonitorOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-1-3Q-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-1-3Q-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_fnf_monitor_on_interface(self):
        result = unconfigure_fnf_monitor_on_interface(self.device, 'GigabitEthernet2/0/3', 'FlowMonitor-1', sampler_name=None, direction='input')
        expected_output = None
        self.assertEqual(result, expected_output)

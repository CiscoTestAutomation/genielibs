import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.debug.configure import debug_software_cpm_switch_pcap


class TestDebugSoftwareCpmSwitchPcap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SA-C9350-24P:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: None
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SA-C9350-24P']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_debug_software_cpm_switch_pcap(self):
        result = debug_software_cpm_switch_pcap(self.device, 'active', 'disable')
        expected_output = None
        self.assertEqual(result, expected_output)

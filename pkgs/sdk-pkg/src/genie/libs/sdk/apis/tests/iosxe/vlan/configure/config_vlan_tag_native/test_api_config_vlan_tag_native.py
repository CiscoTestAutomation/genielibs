import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.configure import config_vlan_tag_native


class TestConfigVlanTagNative(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9500-Core:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9500-Core']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_vlan_tag_native(self):
        result = config_vlan_tag_native(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

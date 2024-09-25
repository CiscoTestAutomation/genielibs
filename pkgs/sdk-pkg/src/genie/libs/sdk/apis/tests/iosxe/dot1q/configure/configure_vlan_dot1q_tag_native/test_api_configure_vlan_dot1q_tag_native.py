import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dot1q.configure import configure_vlan_dot1q_tag_native


class TestConfigureVlanDot1qTagNative(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Raitt:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Raitt']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_vlan_dot1q_tag_native(self):
        result = configure_vlan_dot1q_tag_native(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

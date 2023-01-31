import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ike.configure import configure_modify_ikev2_profile


class TestConfigureModifyIkev2Profile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Hub:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: C8000V
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Hub']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_modify_ikev2_profile(self):
        result = configure_modify_ikev2_profile(self.device, 'IKE-PROF', 'email abc@cisco.com', 'email efg@cisco.com', None, None, 'ppk', 'HUB-KEY', '240')
        expected_output = None
        self.assertEqual(result, expected_output)

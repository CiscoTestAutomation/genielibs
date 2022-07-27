import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_profile


class TestConfigureIkev2Profile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          rad-vtep1:
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
        self.device = self.testbed.devices['rad-vtep1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ikev2_profile(self):
        result = configure_ikev2_profile(self.device, 'ikev2_profile_new', '161.1.1.1', 'pre-share', 'pre-share', 'new_keyring', 10, 2, 'periodic')
        expected_output = None
        self.assertEqual(result, expected_output)

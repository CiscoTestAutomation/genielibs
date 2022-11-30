import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_profile


class TestConfigureIpsecProfile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          fugazi:
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
        self.device = self.testbed.devices['fugazi']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipsec_profile(self):
        result = configure_ipsec_profile(self.device, 'test1', 'test1', None, None, False, False, False, False, False, False, None, False, None, False, None, None, False, None, None, False, None, None, None, None, None, None, False, None, False)
        expected_output = None
        self.assertEqual(result, expected_output)

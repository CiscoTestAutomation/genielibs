import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_profile


class TestConfigureIpsecProfile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          TLS_Mad2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['TLS_Mad2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipsec_profile(self):
        result = configure_ipsec_profile(self.device, 'IPSec_PROFILE', 'IPSec_TRANSFORM', 'IKEv2_PRFOILE', None, True, True, False, False, True, False, 100, True, 20, False, None, None, False, 256, None, True, 'group19', 250, None, None, None, '1.1.1.1', False, None, False)
        expected_output = None
        self.assertEqual(result, expected_output)

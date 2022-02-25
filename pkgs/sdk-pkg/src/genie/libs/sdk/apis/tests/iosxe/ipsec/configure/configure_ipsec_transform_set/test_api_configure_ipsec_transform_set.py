import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_transform_set


class TestConfigureIpsecTransformSet(unittest.TestCase):

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

    def test_configure_ipsec_transform_set(self):
        result = configure_ipsec_transform_set(self.device, 'IPSec_TRANSFORM', 'esp-aes', 'esp-sha512-hmac', 256, True, 'tunnel', False)
        expected_output = None
        self.assertEqual(result, expected_output)

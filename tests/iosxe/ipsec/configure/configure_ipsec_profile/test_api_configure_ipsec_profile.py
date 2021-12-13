import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_profile


class TestConfigureIpsecProfile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          rad-vtep1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['rad-vtep1']
        self.device.connect()

    def test_configure_ipsec_profile(self):
        result = configure_ipsec_profile(self.device, 'ipsec_profile_new', 'transform_set', 'ikev2_profile_new')
        expected_output = None
        self.assertEqual(result, expected_output)

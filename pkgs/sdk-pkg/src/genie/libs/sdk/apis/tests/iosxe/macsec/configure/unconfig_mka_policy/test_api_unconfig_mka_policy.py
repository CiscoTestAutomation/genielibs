import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.macsec.configure import unconfig_mka_policy


class TestUnconfigMkaPolicy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          LG-PK:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['LG-PK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfig_mka_policy(self):
        result = unconfig_mka_policy(self.device, 'TwentyFiveGigE 1/0/7', 'MKA_policy1', True)
        expected_output = None
        self.assertEqual(result, expected_output)

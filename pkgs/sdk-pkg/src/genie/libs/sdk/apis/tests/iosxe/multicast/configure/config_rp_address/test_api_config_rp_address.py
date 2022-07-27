import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import config_rp_address


class TestConfigRpAddress(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          P1:
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
        self.device = self.testbed.devices['P1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_rp_address(self):
        result = config_rp_address(self.device, 'vrf3001', '30.0.1.1')
        expected_output = None
        self.assertEqual(result, expected_output)

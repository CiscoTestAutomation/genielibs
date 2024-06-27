import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_ip_nhrp_map


class TestConfigureIpNhrpMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          router1:
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
        self.device = self.testbed.devices['router1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_nhrp_map(self):
        result = configure_ip_nhrp_map(self.device, 'tu0', '192.162.10.1', '1.1.1.1')
        expected_output = None
        self.assertEqual(result, expected_output)

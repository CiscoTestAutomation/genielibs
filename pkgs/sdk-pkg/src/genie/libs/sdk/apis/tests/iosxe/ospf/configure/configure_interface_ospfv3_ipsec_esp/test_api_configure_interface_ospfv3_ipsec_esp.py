import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_interface_ospfv3_ipsec_esp


class TestConfigureInterfaceOspfv3IpsecEsp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PE-B:
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
        self.device = self.testbed.devices['PE-B']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_ospfv3_ipsec_esp(self):
        result = configure_interface_ospfv3_ipsec_esp(self.device, 'TenGigabitEthernet1/0/41', 25604, 'aes-cbc', '1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78', 'md5', '1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78', 128, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

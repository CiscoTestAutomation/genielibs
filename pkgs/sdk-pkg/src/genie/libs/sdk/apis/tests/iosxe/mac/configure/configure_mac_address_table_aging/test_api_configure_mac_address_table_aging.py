import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mac.configure import configure_mac_address_table_aging


class TestConfigureMacAddressTableAging(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T1-9300-SP1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['T1-9300-SP1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_mac_address_table_aging(self):
        result = configure_mac_address_table_aging(self.device, 30, 'vlan', 201)
        expected_output = None
        self.assertEqual(result, expected_output)

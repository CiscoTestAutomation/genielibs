import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcpv6.get import get_dhcpv6_binding_address_list



class TestGetDHCPv6BindingAddressList(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          VCAT9K-LEAF1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['VCAT9K-LEAF1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_dhcpv6_binding_address_list(self):
        result = get_dhcpv6_binding_address_list(self.device)
        expected_output =  ['2001:103::FDAF:5C5C:AB4D:180']
        self.assertEqual(result, expected_output)

import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.get import get_dhcpv4_binding_address_list



class TestGetDHCPv4BindingAddressList(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          VCAT9K-LEAF1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
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

    def test_get_dhcpv4_server_stats(self):
        result = get_dhcpv4_binding_address_list(self.device)
        expected_output =  ['100.1.0.3', '100.1.0.2', '100.1.0.1']
        self.assertEqual(result, expected_output)

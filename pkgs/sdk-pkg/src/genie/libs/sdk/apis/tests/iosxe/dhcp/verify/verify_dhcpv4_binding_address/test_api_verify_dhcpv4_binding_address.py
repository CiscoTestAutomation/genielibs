import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.verify import verify_dhcpv4_binding_address



class TestVerifyDHCPv4BindingAddress(unittest.TestCase):

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

    def test_verify_dhcpv4_binding_address_true(self):
        result = verify_dhcpv4_binding_address(self.device, '100.1.0.2')
        expected_output =  True
        self.assertEqual(result, expected_output)

    def test_verify_dhcpv4_binding_address_false(self):
        result = verify_dhcpv4_binding_address(self.device, '10.10.10.10')
        expected_output =  False
        self.assertEqual(result, expected_output)

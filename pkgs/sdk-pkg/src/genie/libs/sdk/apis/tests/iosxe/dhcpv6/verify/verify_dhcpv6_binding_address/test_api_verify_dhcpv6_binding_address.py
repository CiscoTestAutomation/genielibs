import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcpv6.verify import verify_dhcpv6_binding_address



class TestVerifyDHCPv6BindingAddress(unittest.TestCase):

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

    def test_verify_dhcpv6_binding_address_true(self):
        result = verify_dhcpv6_binding_address(self.device, '2001:103::FDAF:5C5C:AB4D:180')
        expected_output =  True
        self.assertEqual(result, expected_output)

    def test_verify_dhcpv6_binding_address_false(self):
        result = verify_dhcpv6_binding_address(self.device, '2002:103::FDAF:5C5C:AB4D:180')
        expected_output =  False
        self.assertEqual(result, expected_output)

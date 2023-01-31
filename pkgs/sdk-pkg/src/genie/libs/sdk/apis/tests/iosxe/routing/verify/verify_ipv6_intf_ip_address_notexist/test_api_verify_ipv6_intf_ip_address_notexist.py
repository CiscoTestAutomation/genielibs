import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.verify import verify_ipv6_intf_ip_address_notexist


class TestVerifyIpv6IntfIpAddressNotexist(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          CL4-c9500:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CL4-c9500']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ipv6_intf_ip_address_notexist(self):
        result = verify_ipv6_intf_ip_address_notexist(self.device, 'Vlan1211', '100:12:11::1', 5, 2)
        expected_output = False
        self.assertEqual(result, expected_output)

    def test_verify_ipv6_intf_ip_address_notexist_1(self):
        result = verify_ipv6_intf_ip_address_notexist(self.device, 'Vlan1211', '100:12:11::2', 5, 2)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_ipv6_intf_ip_address_notexist_2(self):
        result = verify_ipv6_intf_ip_address_notexist(self.device, 'Vlan2000', '100:12:11::1', 5, 2)
        expected_output = True
        self.assertEqual(result, expected_output)

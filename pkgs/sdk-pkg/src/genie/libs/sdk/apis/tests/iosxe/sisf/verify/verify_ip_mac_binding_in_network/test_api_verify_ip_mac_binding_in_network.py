import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.verify import verify_ip_mac_binding_in_network


class TestVerifyIpMacBindingInNetwork(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sisf-c9500-11:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-11']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ip_mac_binding_in_network(self):
        result = verify_ip_mac_binding_in_network(self.device, '2001:DB8::105', 'dead.beef.0001', 'ND', '005', None, 60, 10, False)
        expected_output = False
        self.assertEqual(result, expected_output)

    def test_verify_ip_mac_binding_in_network_interface_1(self):
        result = verify_ip_mac_binding_in_network(self.device, '2001:DB8::105', 'dead.beef.0001', 'ND', 5 , None, 60, 10, False, interface="Twe1/0/1")
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_ip_mac_binding_in_network_interface_2(self):
        result = verify_ip_mac_binding_in_network(self.device, '2001:DB8::105', 'dead.beef.0001', 'ND', 5 , None, 60, 10, False, interface="TwentyFiveGigE1/0/1")
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_ip_mac_binding_in_network_interface_3(self):
        result = verify_ip_mac_binding_in_network(self.device, '2002::100', 'ba25.cdf4.ad38', 'L', 100, verify_reachable=True, interface="Vlan20")
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_ip_mac_binding_in_network_interface_4(self):
        result = verify_ip_mac_binding_in_network(self.device, '2002::100', 'ba25.cdf4.ad38', 'L', 100, verify_reachable=True, vlan=20)
        expected_output = True
        self.assertEqual(result, expected_output)

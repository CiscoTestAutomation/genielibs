import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.verify import verify_dhcpv4_packet_received



class TestVerifyDHCPv4PacketReceived(unittest.TestCase):

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

    def test_verify_dhcpv4_packet_received_discover(self):
        result = verify_dhcpv4_packet_received(self.device, 'discover')
        expected_output =  True
        self.assertEqual(result, expected_output)

    def test_verify_dhcpv4_packet_not_received_request(self):
        result = verify_dhcpv4_packet_received(self.device, 'request')
        expected_output =  False
        self.assertEqual(result, expected_output)

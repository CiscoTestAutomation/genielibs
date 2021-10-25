import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.arp.get import get_arp_interface_mac_from_ip


class TestGetArpInterfaceMacFromIp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CGW-laas-c9500-5:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat
            type: cat
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CGW-laas-c9500-5']
        self.device.connect()

    def test_get_arp_interface_mac_from_ip(self):
        result = get_arp_interface_mac_from_ip(self.device, '20.101.1.3', 'vrf101')
        expected_output = ('Vlan101', '0050.5684.0448')
        self.assertEqual(result, expected_output)

import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.arp.verify import verify_arp_vrf_interface_mac_entry


class TestVerifyArpVrfInterfaceMacEntry(unittest.TestCase):

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
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_arp_vrf_interface_mac_entry(self):
        result = verify_arp_vrf_interface_mac_entry(self.device, '20.101.1.3', 'Vlan101', 'vrf101', '0050.5684.0448')
        expected_output = True
        self.assertEqual(result, expected_output)

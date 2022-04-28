import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.utils import clear_dhcpv4_server_stats



class TestClearDHCPv4ServerStats(unittest.TestCase):

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

    def test_clear_dhcpv4_server_stats(self):
        result = clear_dhcpv4_server_stats(device=self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

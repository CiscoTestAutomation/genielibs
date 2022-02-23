import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.arp.configure import unconfigure_ip_arp_inspection_vlan


class TestUnconfigureIpArpInspectionVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          SecG-A3-9410HA:
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
        self.device = self.testbed.devices['SecG-A3-9410HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ip_arp_inspection_vlan(self):
        result = unconfigure_ip_arp_inspection_vlan(self.device, 10)
        expected_output = None
        self.assertEqual(result, expected_output)

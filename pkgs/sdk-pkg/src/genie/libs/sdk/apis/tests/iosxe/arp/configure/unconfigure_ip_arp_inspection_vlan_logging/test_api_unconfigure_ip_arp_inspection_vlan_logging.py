import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.arp.configure import unconfigure_ip_arp_inspection_vlan_logging


class TestUnconfigureIpArpInspectionVlanLogging(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T1-9300-SW1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['T1-9300-SW1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ip_arp_inspection_vlan_logging(self):
        result = unconfigure_ip_arp_inspection_vlan_logging(self.device, '10,20', 'dhcp-bindings', None)
        expected_output = None
        self.assertEqual(result, expected_output)

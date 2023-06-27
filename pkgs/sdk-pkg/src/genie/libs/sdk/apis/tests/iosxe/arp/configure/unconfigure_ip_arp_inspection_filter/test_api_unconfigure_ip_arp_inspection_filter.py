import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.arp.configure import unconfigure_ip_arp_inspection_filter


class TestUnconfigureIpArpInspectionFilter(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SC_9200-2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9200
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SC_9200-2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ip_arp_inspection_filter(self):
        result = unconfigure_ip_arp_inspection_filter(self.device, 'allowed_acl', '10')
        expected_output = None
        self.assertEqual(result, expected_output)

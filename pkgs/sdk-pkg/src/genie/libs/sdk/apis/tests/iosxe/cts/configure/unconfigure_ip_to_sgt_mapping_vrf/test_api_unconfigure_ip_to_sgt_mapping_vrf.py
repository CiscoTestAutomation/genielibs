import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_ip_to_sgt_mapping_vrf


class TestUnconfigureIpToSgtMappingVrf(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          UUT3-macallan:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['UUT3-macallan']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ip_to_sgt_mapping_vrf(self):
        result = unconfigure_ip_to_sgt_mapping_vrf(self.device, 'cisco', '4.4.4.4', 77)
        expected_output = None
        self.assertEqual(result, expected_output)

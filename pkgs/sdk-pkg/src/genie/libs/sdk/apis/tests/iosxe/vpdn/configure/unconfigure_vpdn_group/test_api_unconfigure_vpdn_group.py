import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vpdn.configure import (
    unconfigure_vpdn_group,
    unconfigure_vpdn_group_initiate_to_entries,
    unconfigure_vpdn_l2tp_attribute_initial_received_lcp_confreq,
)


class TestUnconfigureVpdnGroup(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          BB_C8500-12X4QC:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['BB_C8500-12X4QC']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_vpdn_group(self):
        result = unconfigure_vpdn_group(self.device, '11')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_vpdn_group_initiate_to_entries(self):
        result = unconfigure_vpdn_group_initiate_to_entries(
            self.device,
            '1',
            ['10.1.1.1', '10.1.1.2'],
        )
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_vpdn_l2tp_attribute_initial_received_lcp_confreq(self):
        result = unconfigure_vpdn_l2tp_attribute_initial_received_lcp_confreq(
            self.device
        )
        expected_output = None
        self.assertEqual(result, expected_output)

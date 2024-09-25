import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import configure_access_list_extend_with_dst_address_and_gt_port


class TestConfigureAccessListExtendWithDstAddressAndGtPort(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Raitt:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Raitt']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_access_list_extend_with_dst_address_and_gt_port(self):
        result = configure_access_list_extend_with_dst_address_and_gt_port(self.device, 'ACL_1', 70, 'permit', 'udp', 14000, 14449, '206.203.117.19', 2023)
        expected_output = None
        self.assertEqual(result, expected_output)

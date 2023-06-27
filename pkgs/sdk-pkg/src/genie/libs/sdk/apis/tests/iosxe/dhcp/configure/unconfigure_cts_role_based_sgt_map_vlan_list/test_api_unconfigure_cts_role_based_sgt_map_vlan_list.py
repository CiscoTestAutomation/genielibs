import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_cts_role_based_sgt_map_vlan_list


class TestUnconfigureCtsRoleBasedSgtMapVlanList(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9200L
            type: c9200L
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_cts_role_based_sgt_map_vlan_list(self):
        result = unconfigure_cts_role_based_sgt_map_vlan_list(self.device, '300', '300')
        expected_output = None
        self.assertEqual(result, expected_output)

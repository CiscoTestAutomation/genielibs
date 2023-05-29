import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_mac_access_group_mac_acl_in_out


class TestUnconfigureMacAccessGroupMacAclInOut(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          mac-gen2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['mac-gen2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_mac_access_group_mac_acl_in_out(self):
        result = unconfigure_mac_access_group_mac_acl_in_out(self.device, 'TenGigabitEthernet7/0/4', 'pacl1', 'in')
        expected_output = None
        self.assertEqual(result, expected_output)

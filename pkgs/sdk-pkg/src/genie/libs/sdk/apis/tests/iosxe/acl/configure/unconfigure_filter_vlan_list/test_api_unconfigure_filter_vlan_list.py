import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_filter_vlan_list


class TestUnconfigureFilterVlanList(unittest.TestCase):

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

    def test_unconfigure_filter_vlan_list(self):
        result = unconfigure_filter_vlan_list(self.device, 'vacl1', '100')
        expected_output = None
        self.assertEqual(result, expected_output)

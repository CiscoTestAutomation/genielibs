import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.configure import unconfig_vlan_range


class TestUnconfigVlanRange(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          P-R1:
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
        self.device = self.testbed.devices['P-R1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfig_vlan_range(self):
        result = unconfig_vlan_range(self.device, 2, 513, 300)
        expected_output = None
        self.assertEqual(result, expected_output)

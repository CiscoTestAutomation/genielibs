import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nve.configure import unconfig_nve_src_intf

class TestUnconfigNveSrcIntf(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Leaf-01:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Leaf-01']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfig_nve_src_intf(self):
        result = unconfig_nve_src_intf(self.device, "nve 1")
        expected_output = None
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_interface_ospfv3


class TestUnconfigInterfaceOspfv3(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          GD-R5:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat8k
            model: c8000v
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['GD-R5']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfig_interface_ospfv3(self):
        result = unconfig_interface_ospfv3(self.device, 'vmi1', '1', 0, False, True, True)
        expected_output = None
        self.assertEqual(result, expected_output)

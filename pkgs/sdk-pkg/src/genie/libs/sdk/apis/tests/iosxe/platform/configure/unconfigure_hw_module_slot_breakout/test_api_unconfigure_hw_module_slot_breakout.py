import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_hw_module_slot_breakout


class TestUnconfigureHwModuleSlotBreakout(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          TF-C9600-StackWiseVirtual:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['TF-C9600-StackWiseVirtual']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_hw_module_slot_breakout(self):
        result = unconfigure_hw_module_slot_breakout(self.device, 5, 5)
        expected_output = None
        self.assertEqual(result, expected_output)

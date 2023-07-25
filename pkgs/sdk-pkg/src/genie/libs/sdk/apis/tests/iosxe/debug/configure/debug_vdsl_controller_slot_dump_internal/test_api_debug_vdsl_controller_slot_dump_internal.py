import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.debug.configure import debug_vdsl_controller_slot_dump_internal


class TestDebugVdslControllerSlotDumpInternal(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Elixir2:
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
        self.device = self.testbed.devices['Elixir2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_debug_vdsl_controller_slot_dump_internal(self):
        result = debug_vdsl_controller_slot_dump_internal(self.device, '0/0/1', 'sfp_test.dump', 900)
        expected_output = None
        self.assertEqual(result, expected_output)

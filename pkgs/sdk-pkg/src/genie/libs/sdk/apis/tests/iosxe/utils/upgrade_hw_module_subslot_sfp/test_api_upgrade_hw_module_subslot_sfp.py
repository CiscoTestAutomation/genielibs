import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import upgrade_hw_module_subslot_sfp


class TestUpgradeHwModuleSubslotSfp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Elixir_01:
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
        self.device = self.testbed.devices['Elixir_01']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_upgrade_hw_module_subslot_sfp(self):
        result = upgrade_hw_module_subslot_sfp(self.device, '0/0', '0', 'bootflash:dsl-sfp-1_62_8548-dev_elixir.bin', 180)
        expected_output = True
        self.assertEqual(result, expected_output)

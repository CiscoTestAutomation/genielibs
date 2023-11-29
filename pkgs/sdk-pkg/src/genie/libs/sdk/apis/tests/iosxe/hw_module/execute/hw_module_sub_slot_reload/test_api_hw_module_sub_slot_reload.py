import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.hw_module.execute import hw_module_sub_slot_reload


class TestHwModuleSubSlotReload(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          nanook_pkumarmu_rr:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['nanook_pkumarmu_rr']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_hw_module_sub_slot_reload(self):
        result = hw_module_sub_slot_reload(self.device, '0/3')
        expected_output = ''
        self.assertEqual(result, expected_output)

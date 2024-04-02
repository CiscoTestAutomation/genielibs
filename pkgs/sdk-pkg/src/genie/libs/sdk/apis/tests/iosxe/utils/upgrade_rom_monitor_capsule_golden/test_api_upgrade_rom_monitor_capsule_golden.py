import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import upgrade_rom_monitor_capsule_golden


class TestUpgradeRomMonitorCapsuleGolden(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-1-3Q-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-1-3Q-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_upgrade_rom_monitor_capsule_golden(self):
        result = upgrade_rom_monitor_capsule_golden(self.device, 'active', 'R0', 420)
        expected_output = True
        self.assertEqual(result, expected_output)

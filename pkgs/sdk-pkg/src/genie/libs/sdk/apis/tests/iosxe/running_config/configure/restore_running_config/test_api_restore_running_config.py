import os
import unittest
from unittest.mock import ANY, Mock

from pyats.topology import loader

from genie.libs.sdk.apis.iosxe.running_config.configure import restore_running_config


class TestRestoreRunningConfig(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          iolpe2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['iolpe2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_restore_running_config(self):
        result = restore_running_config(self.device, 'unix:', 'base.cfg', 60, False, 300, 30)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_restore_running_config_ignores_incremental_diff_failure(self):
        device = Mock()
        device.execute.side_effect = [
            Exception("diff unsupported"),
            "Rollback Done",
        ]

        result = restore_running_config(
            device, "flash:", "base.cfg", 60, False, 300, 30)

        self.assertTrue(result)
        device.execute.assert_any_call(
            "show archive config incremental-diffs flash:base.cfg")
        device.execute.assert_any_call(
            "configure replace flash:base.cfg",
            reply=ANY,
            timeout=60,
            error_pattern=[],
        )

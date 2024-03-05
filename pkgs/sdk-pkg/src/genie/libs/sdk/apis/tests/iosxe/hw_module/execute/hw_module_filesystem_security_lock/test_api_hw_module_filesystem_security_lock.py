import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.hw_module.execute import hw_module_filesystem_security_lock


class TestHwModuleFilesystemSecurityLock(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ENC:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat8k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ENC']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_hw_module_filesystem_security_lock(self):
        result = hw_module_filesystem_security_lock(self.device, 'bootflash', 'disable')
        expected_output = 'SUCCESS'
        self.assertEqual(result, expected_output)

    def test_hw_module_filesystem_security_lock_1(self):
        result = hw_module_filesystem_security_lock(self.device, 'bootflash', 'enable')
        expected_output = 'SUCCESS'
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import copy_startup_config_from_flash


class TestCopyStartupConfigFromFlash(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          cvvs-9410:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['cvvs-9410']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_copy_startup_config_from_flash(self):
        result = copy_startup_config_from_flash(self.device, 'cvvs-9410-startup.config', 60)
        expected_output = None
        self.assertEqual(result, expected_output)

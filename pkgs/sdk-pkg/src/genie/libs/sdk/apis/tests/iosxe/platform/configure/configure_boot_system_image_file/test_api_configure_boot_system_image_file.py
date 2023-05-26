import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import configure_boot_system_image_file


class TestConfigureBootSystemImageFile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_boot_system_image_file(self):
        result = configure_boot_system_image_file(self.device, 'flash:cat9k-espbase.BLD_POLARIS_DEV_LATEST_20230406_174734.SSA.pkg', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_boot_system_image_file_1(self):
        result = configure_boot_system_image_file(self.device, 'flash:cat9k-espbase.BLD_POLARIS_DEV_LATEST_20230406_174734.SSA.pkg', 'all')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_boot_system_image_file_2(self):
        result = configure_boot_system_image_file(self.device, 'flash:cat9k-espbase.BLD_POLARIS_DEV_LATEST_20230406_174734.SSA.pkg', 2)
        expected_output = None
        self.assertEqual(result, expected_output)

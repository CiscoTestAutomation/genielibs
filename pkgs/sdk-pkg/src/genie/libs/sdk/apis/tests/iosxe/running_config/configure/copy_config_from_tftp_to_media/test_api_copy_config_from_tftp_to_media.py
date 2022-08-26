import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.running_config.configure import copy_config_from_tftp_to_media


class TestCopyConfigFromTftpToMedia(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SPOKE3:
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
        self.device = self.testbed.devices['SPOKE3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_copy_config_from_tftp_to_media(self):
        result = copy_config_from_tftp_to_media(self.device, '202.153.144.25', '/auto/tftp-blr-users3/ashpa/test.txt', 'test.txt', 30, None, 'bootflash')
        expected_output = True
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import delete_directory


class TestDeleteDirectory(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Sanity-ASR2X:
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
        self.device = self.testbed.devices['Sanity-ASR2X']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_delete_directory(self):
        result = delete_directory(self.device, 'bootflash:', 'test')
        expected_output = None
        self.assertEqual(result, expected_output)

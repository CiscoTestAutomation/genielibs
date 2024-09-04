import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.configure import confirm_iox_enabled_requested_storage_media


class TestConfirmIoxEnabledRequestedStorageMedia(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9404R-dut1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9404R-dut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_confirm_iox_enabled_requested_storage_media(self):
        result = confirm_iox_enabled_requested_storage_media(self.device)
        expected_output = True
        self.assertEqual(result, expected_output)

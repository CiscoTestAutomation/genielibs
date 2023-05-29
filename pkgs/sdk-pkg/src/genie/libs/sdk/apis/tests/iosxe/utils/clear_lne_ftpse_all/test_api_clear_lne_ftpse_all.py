import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import clear_lne_ftpse_all


class TestClearLneFtpseAll(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          3900-pagent-3:
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
        self.device = self.testbed.devices['3900-pagent-3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_lne_ftpse_all(self):
        result = clear_lne_ftpse_all(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

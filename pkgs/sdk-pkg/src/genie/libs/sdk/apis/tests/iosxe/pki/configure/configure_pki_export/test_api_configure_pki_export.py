import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pki.configure import configure_pki_export


class TestConfigurePkiExport(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SVL_9500_40X:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SVL_9500_40X']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_pki_export(self):
        result = configure_pki_export(self.device, 'Self', 'pem', 'cisco123', None, None, None, 'terminal', None, None, None, 'aes')
        expected_output = result
        self.assertEqual(result, expected_output)

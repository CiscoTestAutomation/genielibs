import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.macsec.configure import configure_pki_trustpoint


class TestConfigurePkiTrustpoint(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          MSFT_9500QC_BORDER:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['MSFT_9500QC_BORDER']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_pki_trustpoint(self):
        result = configure_pki_trustpoint(self.device, None, 'client', None, 'terminal', None, 'none', None)
        expected_output = None
        self.assertEqual(result, expected_output)

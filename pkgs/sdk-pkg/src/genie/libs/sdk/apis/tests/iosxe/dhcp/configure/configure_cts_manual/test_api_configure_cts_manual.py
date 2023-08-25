import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_cts_manual


class TestConfigureCtsManual(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          VCR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['VCR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_cts_manual(self):
        result = configure_cts_manual(self.device, 'FiftyGigE1/0/1', 'yes', '1234', None, 'yes')
        expected_output = None
        self.assertEqual(result, expected_output)

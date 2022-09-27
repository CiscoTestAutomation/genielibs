import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.lacp.configure import configure_lacp_ratefast


class TestConfigureLacpRatefast(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9300-24UX-2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300-24UX-2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_lacp_ratefast(self):
        result = configure_lacp_ratefast(self.device, 'te1/0/2')
        expected_output = None
        self.assertEqual(result, expected_output)

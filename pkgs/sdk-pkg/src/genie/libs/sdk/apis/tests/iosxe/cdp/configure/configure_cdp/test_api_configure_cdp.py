import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cdp.configure import configure_cdp


class TestConfigureCdp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9300-24UX-1:
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
        self.device = self.testbed.devices['9300-24UX-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_cdp(self):
        result = configure_cdp(self.device, None, 300)
        expected_output = None
        self.assertEqual(result, expected_output)
    
    def test_configure_cdp_1(self):
        result = configure_cdp(self.device, ['TenGigabitEthernet1/0/19', 'TenGigabitEthernet1/0/20'])
        expected_output = None
        self.assertEqual(result, expected_output)

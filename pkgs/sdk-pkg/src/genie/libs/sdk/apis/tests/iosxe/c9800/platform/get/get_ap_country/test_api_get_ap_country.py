import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.get import get_ap_country


class TestGetApCountry(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          vidya-ewlc-5:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9800
            type: wlc
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['vidya-ewlc-5']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_ap_country(self):
        result = get_ap_country(self.device, 'AP188B.4500.44C8')
        expected_output = 'IN'
        self.assertEqual(result, expected_output)

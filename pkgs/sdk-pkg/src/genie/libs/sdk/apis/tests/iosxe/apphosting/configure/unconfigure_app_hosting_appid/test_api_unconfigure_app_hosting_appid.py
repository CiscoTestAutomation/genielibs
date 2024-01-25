import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.configure import unconfigure_app_hosting_appid


class TestUnconfigureAppHostingAppid(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9300-24UX-NBR1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300-24UX-NBR1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_app_hosting_appid(self):
        result = unconfigure_app_hosting_appid(self.device, 'APP')
        expected_output = None
        self.assertEqual(result, expected_output)

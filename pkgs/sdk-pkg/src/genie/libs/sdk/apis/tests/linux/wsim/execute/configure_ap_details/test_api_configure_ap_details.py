import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.wsim.execute import configure_ap_details


class TestConfigureApDetails(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          wsim4ca14d90:~$:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os linux --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: linux
            platform: wsim
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['wsim4ca14d90:~$']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ap_details(self):
        result = configure_ap_details(self.device, 'wsim-AP', '9117', '46', '9.2.45.15', '00:e5:64:00:00:00', '2.4GHz')
        expected_output = None
        self.assertEqual(result, expected_output)

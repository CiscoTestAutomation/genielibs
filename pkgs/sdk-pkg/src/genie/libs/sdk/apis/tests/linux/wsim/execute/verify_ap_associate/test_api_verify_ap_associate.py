import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.wsim.execute import verify_ap_associate


class TestVerifyApAssociate(unittest.TestCase):

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

    def test_verify_ap_associate(self):
        result = verify_ap_associate(self.device, '1', 600)
        expected_output = None
        self.assertEqual(result, expected_output)

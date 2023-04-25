import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import verify_ping


class TestVerifyPing(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          iolpe2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['iolpe2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ping(self):
        result = verify_ping(self.device, '1.1.1.8', 100, 1, None, None, None, 60, 10, None)
        expected_output = True
        self.assertEqual(result, expected_output)

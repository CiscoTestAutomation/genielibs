import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.macsec.verify import verify_mka_session


class TestVerifyMkaSession(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Skyfox-svl:
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
        self.device = self.testbed.devices['Skyfox-svl']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_mka_session(self):
        result = verify_mka_session(self.device, 'HundredGigE1/0/23', 'INITIALIZING', None, 160, None)
        expected_output = True
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dot1x.verify import verify_no_access_session


class TestVerifyNoAccessSession(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          E-9300-STACK:
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
        self.device = self.testbed.devices['E-9300-STACK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_no_access_session(self):
        result = verify_no_access_session(self.device, 'GigabitEthernet4/0/10')
        expected_output = False
        self.assertEqual(result, expected_output)

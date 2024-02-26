import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.socat.relay import stop_socat_relay


class TestStopSocatRelay(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          linux-server:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os linux --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: linux
            platform: linux
            type: linux
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['linux-server']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_stop_socat_relay(self):
        result = stop_socat_relay(self.device, '3240462')
        expected_output = None
        self.assertEqual(result, expected_output)

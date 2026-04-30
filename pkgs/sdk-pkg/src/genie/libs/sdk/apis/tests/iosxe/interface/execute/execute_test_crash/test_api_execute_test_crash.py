import os
import unittest
from unittest.mock import patch
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.execute import execute_test_crash


class TestExecuteTestCrash(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          startrek-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300X
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['startrek-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_test_crash(self):
        """Test that execute_test_crash uses _disconnect_reconnect after crash."""
        with patch('genie.libs.sdk.apis.iosxe.interface.execute._disconnect_reconnect',
                   return_value=True) as mock_reconnect, \
             patch('genie.libs.sdk.apis.iosxe.interface.execute.time') as mock_time:
            execute_test_crash(self.device, '6', 500, 200)
            mock_time.sleep.assert_called_once_with(200)
            mock_reconnect.assert_called_once_with(self.device)


import os
import datetime
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.get import get_logging_message_time


class TestGetLoggingMessageTime(TestCase):
    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9407R-dut1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9407R-dut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_logging_message_time(self):
        result = get_logging_message_time(self.device, ('Apr 8 04:18:45.753: %LINEPROTO-5-UPDOWN: Line protocol on Interface '
 'GigabitEthernet2/0/21, changed state to up'))
        expected_output = datetime.datetime(2025, 4, 8, 4, 18, 45, 753)
        self.assertEqual(result, expected_output)

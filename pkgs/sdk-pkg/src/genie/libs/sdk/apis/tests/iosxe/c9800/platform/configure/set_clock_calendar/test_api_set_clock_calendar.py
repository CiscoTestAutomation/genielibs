import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.configure import set_clock_calendar


class TestSetClockCalendar(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          vidya-ewlc-5:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
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

    def test_set_clock_calendar(self):
        result = set_clock_calendar(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

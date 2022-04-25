import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.configure import clear_device_tracking_messages


class TestClearDeviceTrackingMessages(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sisf-c9500-11:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: ios
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-11']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_device_tracking_messages(self):
        result = clear_device_tracking_messages(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

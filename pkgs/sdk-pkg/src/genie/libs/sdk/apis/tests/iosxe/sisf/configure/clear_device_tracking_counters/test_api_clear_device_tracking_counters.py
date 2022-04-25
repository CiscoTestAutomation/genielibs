import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.configure import clear_device_tracking_counters


class TestClearDeviceTrackingCounters(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sisf-c9500-21-8-26-2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ios
            type: ios
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-21-8-26-2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_device_tracking_counters(self):
        result = clear_device_tracking_counters(device=self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_counters_1(self):
        result = clear_device_tracking_counters(device=self.device, interface='Ethernet1/0')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_counters_2(self):
        result = clear_device_tracking_counters(device=self.device, vlan='200')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_counters_3(self):
        result = clear_device_tracking_counters(device=self.device, bdi='200')
        expected_output = None
        self.assertEqual(result, expected_output)


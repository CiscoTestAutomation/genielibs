import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.device_sensor.configure import unconfigure_device_sensor_filter_list


class TestUnconfigureDeviceSensorFilterList(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_device_sensor_filter_list(self):
        result = unconfigure_device_sensor_filter_list(self.device, 'cdp', 'lisds', 'device-name', None, None, None, False)
        expected_output = None
        self.assertEqual(result, expected_output)

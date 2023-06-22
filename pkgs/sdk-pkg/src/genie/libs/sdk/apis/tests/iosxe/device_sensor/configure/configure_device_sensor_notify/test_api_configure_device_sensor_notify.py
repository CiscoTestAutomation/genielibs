import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.device_sensor.configure import configure_device_sensor_notify


class TestConfigureDeviceSensorNotify(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ECR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ECR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_device_sensor_notify(self):
        result = configure_device_sensor_notify(self.device, 'all-changes')
        expected_output = None
        self.assertEqual(result, expected_output)

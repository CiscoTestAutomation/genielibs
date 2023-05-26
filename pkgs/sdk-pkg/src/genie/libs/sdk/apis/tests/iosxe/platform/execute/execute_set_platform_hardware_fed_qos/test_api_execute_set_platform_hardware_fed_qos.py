import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_set_platform_hardware_fed_qos


class TestExecuteSetPlatformHardwareFedQos(unittest.TestCase):

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
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['startrek-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_set_platform_hardware_fed_qos(self):
        result = execute_set_platform_hardware_fed_qos(self.device, 'active', 'multicast', 'Hu1/0/5', 'switch', 5, 'attach')
        expected_output = None
        self.assertEqual(result, expected_output)

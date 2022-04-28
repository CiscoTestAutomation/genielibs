import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_clear_platform_hardware_fed_active_qos_statistics_interface


class TestExecuteClearPlatformHardwareFedActiveQosStatisticsInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          dhamu_skyfox:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['dhamu_skyfox']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_clear_platform_hardware_fed_active_qos_statistics_interface(self):
        result = execute_clear_platform_hardware_fed_active_qos_statistics_interface(self.device, 'Hu1/0/5')
        expected_output = None
        self.assertEqual(result, expected_output)

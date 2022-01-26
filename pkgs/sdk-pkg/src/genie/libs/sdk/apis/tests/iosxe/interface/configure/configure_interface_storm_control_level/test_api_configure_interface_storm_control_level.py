import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_storm_control_level


class TestConfigureInterfaceStormControlLevel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Overlord1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: isr4k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Overlord1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_storm_control_level(self):
        result = configure_interface_storm_control_level(self.device, 'GigabitEthernet1/0/2', 'unicast', 7, '', '')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_interface_storm_control_level_1(self):
        result = configure_interface_storm_control_level(self.device, 'GigabitEthernet1/0/2', 'broadcast', 7, 4, '')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_interface_storm_control_level_2(self):
        result = configure_interface_storm_control_level(self.device, 'GigabitEthernet1/0/2', 'multicast', 1000, 990, 'pps')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_interface_storm_control_level_3(self):
        result = configure_interface_storm_control_level(self.device, 'GigabitEthernet1/0/2', 'unicast', 10000, 9990, 'bps')
        expected_output = None
        self.assertEqual(result, expected_output)

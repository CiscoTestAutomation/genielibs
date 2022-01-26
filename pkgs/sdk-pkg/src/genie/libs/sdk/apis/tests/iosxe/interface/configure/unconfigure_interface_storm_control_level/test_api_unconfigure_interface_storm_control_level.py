import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_storm_control_level


class TestUnconfigureInterfaceStormControlLevel(unittest.TestCase):

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

    def test_unconfigure_interface_storm_control_level(self):
        result = unconfigure_interface_storm_control_level(self.device, 'GigabitEthernet1/0/2', 'unicast')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_interface_storm_control_level_1(self):
        result = unconfigure_interface_storm_control_level(self.device, 'GigabitEthernet1/0/2', 'broadcast')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_interface_storm_control_level_2(self):
        result = unconfigure_interface_storm_control_level(self.device, 'GigabitEthernet1/0/2', 'multicast')
        expected_output = None
        self.assertEqual(result, expected_output)

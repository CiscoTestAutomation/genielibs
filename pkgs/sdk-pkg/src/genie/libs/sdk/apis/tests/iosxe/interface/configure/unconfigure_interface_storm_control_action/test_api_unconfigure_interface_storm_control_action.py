import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_storm_control_action


class TestUnconfigureInterfaceStormControlAction(unittest.TestCase):

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

    def test_unconfigure_interface_storm_control_action(self):
        result = unconfigure_interface_storm_control_action(self.device, 'GigabitEthernet1/0/2', 'shutdown')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_interface_storm_control_action_1(self):
        result = unconfigure_interface_storm_control_action(self.device, 'GigabitEthernet1/0/2', 'trap')
        expected_output = None
        self.assertEqual(result, expected_output)

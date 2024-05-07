import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_switchport_pvlan_mode


class TestConfigureInterfaceSwitchportPvlanMode(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sw6:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat3k
            model: c3850
            type: c3850
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sw6']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_switchport_pvlan_mode(self):
        result = configure_interface_switchport_pvlan_mode(device=self.device, interface='GigabitEthernet1/0/11', mode='host')
        expected_output = None
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_range_switchport_mode


class TestConfigureInterfaceRangeSwitchportMode(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          mac-gen1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['mac-gen1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_range_switchport_mode(self):
        result = configure_interface_range_switchport_mode(self.device, 'GigabitEthernet5/0/34', 'trunk')
        expected_output = None
        self.assertEqual(result, expected_output)

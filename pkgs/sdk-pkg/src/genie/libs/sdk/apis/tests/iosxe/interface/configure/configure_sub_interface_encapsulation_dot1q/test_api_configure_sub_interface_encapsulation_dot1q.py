import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_sub_interface_encapsulation_dot1q


class TestConfigureSubInterfaceEncapsulationDot1q(unittest.TestCase):

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

    def test_configure_sub_interface_encapsulation_dot1q(self):
        result = configure_sub_interface_encapsulation_dot1q(self.device, 'GigabitEthernet5/0/33', '2', '5.1.2.2', '255.255.255.0')
        expected_output = None
        self.assertEqual(result, expected_output)

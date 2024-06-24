import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_dot1q_ethertype


class TestConfigureInterfaceDot1qEthertype(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Fry_06:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Fry_06']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_dot1q_ethertype(self):
        result = configure_interface_dot1q_ethertype(self.device, 'GigabitEthernet0/0/0', '0x88A8')
        expected_output = None
        self.assertEqual(result, expected_output)

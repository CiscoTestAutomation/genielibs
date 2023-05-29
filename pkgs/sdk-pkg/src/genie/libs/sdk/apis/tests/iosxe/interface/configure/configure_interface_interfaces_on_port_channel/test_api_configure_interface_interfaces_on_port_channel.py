import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_interfaces_on_port_channel


class TestConfigureInterfaceInterfacesOnPortChannel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          A1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['A1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_interfaces_on_port_channel(self):
        result = configure_interface_interfaces_on_port_channel(self.device, 'g1/0/13', 'desirable', 10, ['g1/0/13', 'g4/0/25', 'g4/0/37'])
        expected_output = None
        self.assertEqual(result, expected_output)

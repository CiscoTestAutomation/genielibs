import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import no_shut_interface_range


class TestNoShutInterfaceRange(unittest.TestCase):

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

    def test_no_shut_interface_range(self):
        result = no_shut_interface_range(self.device, 'vlan', 2, 513)
        expected_output = None
        self.assertEqual(result, expected_output)

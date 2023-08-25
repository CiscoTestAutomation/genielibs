import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.clear import clear_interface_range


class TestClearInterfaceRange(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          P-R1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['P-R1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_interface_range(self):
        result = clear_interface_range(self.device, 'Loopback', '10-500')
        expected_output = None
        self.assertEqual(result, expected_output)

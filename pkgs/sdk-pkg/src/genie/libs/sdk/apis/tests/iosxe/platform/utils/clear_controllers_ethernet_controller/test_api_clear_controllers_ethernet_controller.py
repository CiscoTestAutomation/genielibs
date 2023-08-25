import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.utils import clear_controllers_ethernet_controller


class TestClearControllersEthernetController(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T1-9300-SP1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['T1-9300-SP1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_controllers_ethernet_controller(self):
        result = clear_controllers_ethernet_controller(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

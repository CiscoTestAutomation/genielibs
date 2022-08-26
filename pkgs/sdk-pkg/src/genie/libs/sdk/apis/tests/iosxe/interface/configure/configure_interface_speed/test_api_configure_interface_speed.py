import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_speed


class TestConfigureInterfaceSpeed(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          1783-CMS20DN:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: s5k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['1783-CMS20DN']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_speed(self):
        result = configure_interface_speed(self.device, 'GigabitEthernet1/2', '10')
        expected_output = None
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_service_policy


class TestUnconfigureInterfaceServicePolicy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Raitt:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Raitt']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_interface_service_policy(self):
        result = unconfigure_interface_service_policy(self.device, 'GigabitEthernet1/0/1', 'pm-tb1', 'input')
        expected_output = None
        self.assertEqual(result, expected_output)

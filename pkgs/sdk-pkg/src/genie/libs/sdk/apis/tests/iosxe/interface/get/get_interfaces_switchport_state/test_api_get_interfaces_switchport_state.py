import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_interfaces_switchport_state


class TestGetInterfacesSwitchportState(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          1783-HMS4EG8CGR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ie3k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['1783-HMS4EG8CGR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_interfaces_switchport_state(self):
        result = get_interfaces_switchport_state(self.device, 'GigabitEthernet1/6')
        expected_output = True
        self.assertEqual(result, expected_output)

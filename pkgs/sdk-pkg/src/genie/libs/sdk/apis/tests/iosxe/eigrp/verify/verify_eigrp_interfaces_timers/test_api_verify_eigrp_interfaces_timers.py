import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eigrp.verify import verify_eigrp_interfaces_timers


class TestVerifyEigrpInterfacesTimers(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          R1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_eigrp_interfaces_timers(self):
        result = verify_eigrp_interfaces_timers(self.device, {'FastEthernet0/0': [{'hello_interval': 5}, {'hold_time': 15}]}, 'default', 1, 'ipv4', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)

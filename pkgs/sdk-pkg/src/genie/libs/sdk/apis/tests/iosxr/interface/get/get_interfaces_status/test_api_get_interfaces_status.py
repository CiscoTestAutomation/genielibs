import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxr.interface.get import get_interfaces_status


class TestGetInterfacesStatus(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          R2_xr:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxr --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxr
            platform: iosxrv9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R2_xr']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_interfaces_status(self):
        result = get_interfaces_status(self.device)
        expected_output = {
            'Bundle-Ether12': 'Down',
            'Bundle-Ether23': 'Down',
            'Loopback0': 'Up',
            'Loopback300': 'Up',
            'MgmtEth0/RP0/CPU0/0': 'Shutdown'}
        self.assertEqual(result, expected_output)

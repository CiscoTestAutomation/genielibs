import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxr.interface.configure import configure_interfaces_unshutdown


class TestConfigureInterfacesUnshutdown(unittest.TestCase):

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

    def test_configure_interfaces_unshutdown(self):
        result = configure_interfaces_unshutdown(self.device, ['GigabitEthernet0/0/0/0'])
        expected_output = None
        self.assertEqual(result, expected_output)

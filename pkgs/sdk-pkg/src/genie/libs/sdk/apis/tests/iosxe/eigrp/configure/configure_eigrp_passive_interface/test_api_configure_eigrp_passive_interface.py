import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eigrp.configure import configure_eigrp_passive_interface


class TestConfigureEigrpPassiveInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Speedracer-Sanity:
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
        self.device = self.testbed.devices['Speedracer-Sanity']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_eigrp_passive_interface(self):
        result = configure_eigrp_passive_interface(self.device, '1', ['GigabitEthernet0/0/0'])
        expected_output = None
        self.assertEqual(result, expected_output)

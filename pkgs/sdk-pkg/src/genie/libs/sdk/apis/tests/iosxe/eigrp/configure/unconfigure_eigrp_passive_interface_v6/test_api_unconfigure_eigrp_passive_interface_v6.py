import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eigrp.configure import unconfigure_eigrp_passive_interface_v6


class TestUnconfigureEigrpPassiveInterfaceV6(unittest.TestCase):

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

    def test_unconfigure_eigrp_passive_interface_v6(self):
        result = unconfigure_eigrp_passive_interface_v6(self.device, '1', ['GigabitEthernet0/0/0'])
        expected_output = None
        self.assertEqual(result, expected_output)

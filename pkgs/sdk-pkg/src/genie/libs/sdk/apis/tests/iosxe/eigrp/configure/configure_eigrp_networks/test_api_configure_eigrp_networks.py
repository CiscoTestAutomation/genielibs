import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eigrp.configure import configure_eigrp_networks


class TestConfigureEigrpNetworks(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          mac-gen2:
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
        self.device = self.testbed.devices['mac-gen2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_eigrp_networks(self):
        result = configure_eigrp_networks(self.device, '10', ['100.100.0.0'], '255.255.0.0', '1.1.1.1', 'all-interfaces', passive_interfaces=['GigabitEthernet0/0/0', 'GigabitEthernet0/0/1'])
        expected_output = None
        self.assertEqual(result, expected_output)

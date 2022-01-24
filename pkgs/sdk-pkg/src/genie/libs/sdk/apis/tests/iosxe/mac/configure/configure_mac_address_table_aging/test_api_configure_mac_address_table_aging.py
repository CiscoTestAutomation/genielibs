import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mac.configure import configure_mac_address_table_aging


class TestConfigureMacAddressTableAging(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_mac_address_table_aging(self):
        result = configure_mac_address_table_aging(device=self.device, aging_time=1800)
        expected_output = None
        self.assertEqual(result, expected_output)

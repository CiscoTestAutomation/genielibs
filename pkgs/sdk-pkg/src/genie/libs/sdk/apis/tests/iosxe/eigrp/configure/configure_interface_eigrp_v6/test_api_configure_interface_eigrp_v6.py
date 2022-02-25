import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eigrp.configure import configure_interface_eigrp_v6


class TestConfigureInterfaceEigrpV6(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9300x-A:
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
        self.device = self.testbed.devices['9300x-A']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_eigrp_v6(self):
        result = configure_interface_eigrp_v6(self.device, ['TenGigabitEthernet1/0/1'], '66')
        expected_output = None
        self.assertEqual(result, expected_output)

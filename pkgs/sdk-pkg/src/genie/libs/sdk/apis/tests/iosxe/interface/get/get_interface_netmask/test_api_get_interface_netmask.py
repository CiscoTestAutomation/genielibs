import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_netmask


class TestGetInterfaceNetmask(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R1_xe:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: CSR1000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1_xe']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_interface_netmask(self):
        result = get_interface_netmask('172.16.1.139')
        expected_output = '/16'
        self.assertEqual(result, expected_output)

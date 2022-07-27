import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.interface.get import get_interface_ipv4_address


class TestGetInterfaceIpv4Address(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R3_nx:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir mock_data --state connect
                protocol: unknown
            os: nxos
            platform: n9kv
            type: NX-OSv 9000
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R3_nx']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_interface_ipv4_address(self):
        result = get_interface_ipv4_address(self.device, 'mgmt0')
        expected_output = '172.16.1.213/24'
        self.assertEqual(result, expected_output)

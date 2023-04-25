import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nve.get import get_nve_interface_tunnel

class TestGetNveInterfaceTunnel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          PE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_nve_interface_tunnel(self):
        result = get_nve_interface_tunnel(self.device, 'nve 1')
        expected_output = 'Tunnel0'
        self.assertEqual(result, expected_output)

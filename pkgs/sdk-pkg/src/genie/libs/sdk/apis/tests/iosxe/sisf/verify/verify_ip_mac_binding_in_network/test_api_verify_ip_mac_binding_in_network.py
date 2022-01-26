import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.verify import verify_ip_mac_binding_in_network


class TestVerifyIpMacBindingInNetwork(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sisf-c9500-11:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-11']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ip_mac_binding_in_network(self):
        result = verify_ip_mac_binding_in_network(self.device, '2001:DB8::105', 'dead.beef.0001', 'ND', '005', None, 60, 10, False)
        expected_output = False
        self.assertEqual(result, expected_output)

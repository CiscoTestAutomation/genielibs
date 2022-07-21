import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.verify import verify_routing_subnet_entry


class TestVerifyRoutingSubnetEntry(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CGW-laas-c9500-5:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat
            type: cat
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CGW-laas-c9500-5']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_routing_subnet_entry(self):
        result = verify_routing_subnet_entry(self.device, '20.101.1.0', 'vrf101')
        expected_output = True
        self.assertEqual(result, expected_output)

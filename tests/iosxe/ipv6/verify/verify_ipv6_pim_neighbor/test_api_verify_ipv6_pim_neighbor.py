import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipv6.verify import verify_ipv6_pim_neighbor


class TestVerifyIpv6PimNeighbor(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Intrepid-DUT-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid-DUT-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ipv6_pim_neighbor(self):
        result = verify_ipv6_pim_neighbor(self.device, 'TwoH5/0/41', 'FE80::2A7:42FF:FE9B:D35F', 15, 5)
        expected_output = True
        self.assertEqual(result, expected_output)

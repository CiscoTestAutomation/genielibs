import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ospf.configure import unconfigure_ip_prefix_list


class TestUnconfigureIpPrefixList(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9400_L2_DUT:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9400_L2_DUT']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ip_prefix_list(self):
        result = unconfigure_ip_prefix_list(self.device, 'up', 1, '1.1.1.1', 32)
        expected_output = None
        self.assertEqual(result, expected_output)

import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_static_nat_network_rule


class TestUnconfigureStaticNatNetworkRule(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          SF-W11-SVL:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SF-W11-SVL']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_static_nat_network_rule(self):
        result = unconfigure_static_nat_network_rule(self.device, '35.0.0.0', '81.1.1.0', '255.255.255.0')
        expected_output = None
        self.assertEqual(result, expected_output)

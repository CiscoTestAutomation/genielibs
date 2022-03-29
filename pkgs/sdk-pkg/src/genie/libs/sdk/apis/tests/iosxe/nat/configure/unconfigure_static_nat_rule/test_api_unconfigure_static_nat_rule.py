import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_static_nat_rule


class TestUnconfigureStaticNatRule(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          FE2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['FE2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_static_nat_rule(self):
        result = unconfigure_static_nat_rule(self.device, '21.21.21.22', '21.21.21.22', 'udp', 500, 600, True)
        expected_output = None
        self.assertEqual(result, expected_output)

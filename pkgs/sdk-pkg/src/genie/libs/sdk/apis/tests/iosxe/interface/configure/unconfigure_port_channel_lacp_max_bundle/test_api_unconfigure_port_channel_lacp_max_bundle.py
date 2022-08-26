import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_port_channel_lacp_max_bundle


class TestUnconfigurePortChannelLacpMaxBundle(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Cat9600HA_DUT1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Cat9600HA_DUT1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_port_channel_lacp_max_bundle(self):
        result = unconfigure_port_channel_lacp_max_bundle(self.device, '100', '1')
        expected_output = None
        self.assertEqual(result, expected_output)
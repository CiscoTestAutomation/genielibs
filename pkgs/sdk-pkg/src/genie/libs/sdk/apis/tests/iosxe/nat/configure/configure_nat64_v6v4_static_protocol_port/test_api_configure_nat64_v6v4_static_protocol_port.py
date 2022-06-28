import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat64_v6v4_static_protocol_port


class TestConfigureNat64V6v4StaticProtocolPort(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Starfleet:
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
        self.device = self.testbed.devices['Starfleet']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_nat64_v6v4_static_protocol_port(self):
        result = configure_nat64_v6v4_static_protocol_port(self.device, 'tcp', '2001:1::2', 1234, '1.1.1.2', 100)
        expected_output = None
        self.assertEqual(result, expected_output)

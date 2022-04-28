import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eigrp.configure import configure_eigrp_named_networks


class TestConfigureEigrpNamedNetworks(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          kparames_csr10:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c8000v
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['kparames_csr10']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_eigrp_named_networks(self):
        result = configure_eigrp_named_networks(self.device, 'named-eigrp', 200, ['11.11.11.0', '11.11.12.0'], '255.255.255.0', None, 'ipv4', 'test', 'unicast')
        expected_output = None
        self.assertEqual(result, expected_output)

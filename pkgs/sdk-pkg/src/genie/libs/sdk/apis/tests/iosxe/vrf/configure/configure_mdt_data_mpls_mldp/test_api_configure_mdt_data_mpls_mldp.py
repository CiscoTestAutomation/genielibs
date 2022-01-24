import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_mdt_data_mpls_mldp


class TestConfigureMdtDataMplsMldp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          P2:
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
        self.device = self.testbed.devices['P2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_mdt_data_mpls_mldp(self):
        result = configure_mdt_data_mpls_mldp(device=self.device, vrf_name='vrf3001', address_family='ipv4', mdt_data=10)
        expected_output = None
        self.assertEqual(result, expected_output)

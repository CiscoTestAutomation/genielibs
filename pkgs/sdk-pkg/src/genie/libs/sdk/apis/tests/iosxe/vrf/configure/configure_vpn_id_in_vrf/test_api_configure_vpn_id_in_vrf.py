import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_vpn_id_in_vrf


class TestConfigureVpnIdInVrf(unittest.TestCase):

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

    def test_configure_vpn_id_in_vrf(self):
        result = configure_vpn_id_in_vrf(device=self.device, vrf_name='vrf3001', vpn_id='3001:1')
        expected_output = None
        self.assertEqual(result, expected_output)

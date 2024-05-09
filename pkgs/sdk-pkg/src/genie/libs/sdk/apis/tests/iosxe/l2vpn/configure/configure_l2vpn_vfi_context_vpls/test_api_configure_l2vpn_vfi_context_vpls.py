import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.l2vpn.configure import configure_l2vpn_vfi_context_vpls


class TestConfigureL2vpnVfiContextVpls(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Prometheus:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Prometheus']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_l2vpn_vfi_context_vpls(self):
        result = configure_l2vpn_vfi_context_vpls(self.device, '10', None, 'True', '10')
        expected_output = None
        self.assertEqual(result, expected_output)

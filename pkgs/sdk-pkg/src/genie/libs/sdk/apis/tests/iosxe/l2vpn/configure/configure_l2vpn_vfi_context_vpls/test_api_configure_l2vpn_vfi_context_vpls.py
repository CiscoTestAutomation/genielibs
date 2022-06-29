import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.l2vpn.configure import configure_l2vpn_vfi_context_vpls


class TestConfigureL2vpnVfiContextVpls(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          PE1:
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
        self.device = self.testbed.devices['PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_l2vpn_vfi_context_vpls(self):
        result = configure_l2vpn_vfi_context_vpls(self.device, 111, None, 1)
        expected_output = None
        self.assertEqual(result, expected_output)

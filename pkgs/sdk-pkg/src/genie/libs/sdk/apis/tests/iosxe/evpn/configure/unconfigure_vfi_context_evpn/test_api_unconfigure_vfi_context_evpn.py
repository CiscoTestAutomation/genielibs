import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.evpn.configure import unconfigure_vfi_context_evpn


class TestUnconfigureVfiContextEvpn(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T3-9500-S2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['T3-9500-S2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_vfi_context_evpn(self):
        result = unconfigure_vfi_context_evpn(self.device, 'VFI201')
        expected_output = None
        self.assertEqual(result, expected_output)

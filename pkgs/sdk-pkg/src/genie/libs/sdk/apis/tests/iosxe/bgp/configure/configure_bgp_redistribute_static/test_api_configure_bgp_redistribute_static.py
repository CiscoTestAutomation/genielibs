import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_redistribute_static


class TestConfigureBgpRedistributeStatic(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          iolpe2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iol
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['iolpe2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_bgp_redistribute_static(self):
        result = configure_bgp_redistribute_static(self.device, 65000, 'vpnv4', None, 'test')
        expected_output = None
        self.assertEqual(result, expected_output)

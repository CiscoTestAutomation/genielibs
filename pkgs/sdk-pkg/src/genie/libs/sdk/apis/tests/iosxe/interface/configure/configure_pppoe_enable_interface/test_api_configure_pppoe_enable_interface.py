import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_pppoe_enable_interface


class TestConfigurePppoeEnableInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          C1113-8P_pkumarmu:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['C1113-8P_pkumarmu']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_pppoe_enable_interface(self):
        result = configure_pppoe_enable_interface(self.device, 'Ethernet0/2/0', 'global', '100', '1590')
        expected_output = None
        self.assertEqual(result, expected_output)

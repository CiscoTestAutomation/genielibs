import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_ip_on_atm_interface


class TestConfigureIpOnAtmInterface(unittest.TestCase):

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

    def test_configure_ip_on_atm_interface(self):
        result = configure_ip_on_atm_interface(self.device, 'ATM0/2/0', '10/100', '10', '10.10.11.11', '255.255.255.0', '5000::1/64', 'aal5snap', 'ppp', '1', 'vbr-rt', 500, '500', '1')
        expected_output = None
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.qos.configure import configure_ip_access_list_with_dscp_on_device


class TestConfigureIpAccessListWithDscpOnDevice(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Raitt:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Raitt']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_access_list_with_dscp_on_device(self):
        result = configure_ip_access_list_with_dscp_on_device(self.device, 100, 10, 'permit', '131.1.1.2', '162.1.1.2', '7')
        expected_output = None
        self.assertEqual(result, expected_output)

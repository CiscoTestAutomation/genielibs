import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_appid_iperf_from_vlan


class TestConfigureAppHostingAppidIperfFromVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9200
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_app_hosting_appid_iperf_from_vlan(self):
        result = configure_app_hosting_appid_iperf_from_vlan(self.device, 1, '15')
        expected_output = None
        self.assertEqual(result, expected_output)

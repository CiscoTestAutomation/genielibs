import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import config_standard_acl_for_ip_pim


class TestConfigStandardAclForIpPim(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          P1:
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
        self.device = self.testbed.devices['P1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_standard_acl_for_ip_pim(self):
        result = config_standard_acl_for_ip_pim(self.device, 'vrf3001-BidigroupRP', 'permit', '229.1.1.1', '0.0.255.255', 'vrf3001', '30.0.1.1', True)
        expected_output = None
        self.assertEqual(result, expected_output)

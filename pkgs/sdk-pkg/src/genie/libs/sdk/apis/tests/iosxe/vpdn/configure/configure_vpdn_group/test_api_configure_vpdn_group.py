import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vpdn.configure import configure_vpdn_group


class TestConfigureVpdnGroup(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          BB_C8500-12X4QC:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['BB_C8500-12X4QC']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_vpdn_group(self):
        result = configure_vpdn_group(self.device, True, '11', False, True, 'cisco.com', '9.9.9.1', '0', 'cisco', '1', 'lns1')
        expected_output = None
        self.assertEqual(result, expected_output)

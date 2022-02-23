import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_coa


class TestConfigureCoa(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9400_L2_DUT:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9400_L2_DUT']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_coa(self):
        result = configure_coa(self.device, {'hostname': '100.8.12.110', 'server_key': 'cisco123', 'vrf': 'cwa'})
        expected_output = None
        self.assertEqual(result, expected_output)

import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mdns.configure import configure_default_mdns_controller


class TestConfigureDefaultMdnsController(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          C9500H_Sathya:
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
        self.device = self.testbed.devices['C9500H_Sathya']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_default_mdns_controller(self):
        result = configure_default_mdns_controller(self.device, 'DNAC', '98.98.98.10', 'TwentyFiveGigE1/0/1', 'cntrl_list', 'all', 'cntrl_policy', 'any')
        expected_output = None
        self.assertEqual(result, expected_output)

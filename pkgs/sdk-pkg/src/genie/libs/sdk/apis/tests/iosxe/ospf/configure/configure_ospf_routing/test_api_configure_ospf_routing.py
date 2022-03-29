import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_routing


class TestConfigureOspfRouting(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          C9404R_HA:
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
        self.device = self.testbed.devices['C9404R_HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ospf_routing(self):
        result = configure_ospf_routing(self.device, 1, 'None', False, True, 'cisco', True, 'debug detail', 'None', 'None')
        expected_output = None
        self.assertEqual(result, expected_output)

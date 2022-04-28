import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_routing


class TestConfigureOspfRouting(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          kparames_csr10:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c8000v
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['kparames_csr10']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ospf_routing(self):
        result = configure_ospf_routing(self.device, 200, None, False, True, 'cisco', True, 'debug detail', None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

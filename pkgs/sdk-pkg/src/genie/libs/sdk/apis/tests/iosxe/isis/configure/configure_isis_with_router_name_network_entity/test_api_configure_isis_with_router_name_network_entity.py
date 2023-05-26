import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.isis.configure import configure_isis_with_router_name_network_entity


class TestConfigureIsisWithRouterNameNetworkEntity(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          TSN-2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['TSN-2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_isis_with_router_name_network_entity(self):
        result = configure_isis_with_router_name_network_entity(self.device, 'tag1', '49.0000.1720.1604.2222.00', None, None, None, 'all-interfaces', 'log-adjacency-changes', 'ietf', 'wide')
        expected_output = None
        self.assertEqual(result, expected_output)
